import pandas as pd
import numpy as np
import re
from dateutil.relativedelta import relativedelta


class ChqCols:
    uid = "DealUID"
    payment_discipline = "PaymentDiscipline"
    payment_discipline_cleansed = "payment_discipline_cleansed"
    deal_type = "LoanKindCode"
    partner_type = "BCHPartnerType"
    loan_status = "CreditStatus"
    date_of_factual_closure = "CloseDtFact"
    ch_relevance_date = "ApplicationDate"
    loan_relevance_date = "LastUpdateDt"


class PaymentDisciplineSymbols:
    FINAL = "BCIRSTW"
    FINAL_W_OVERDUE = "BIRSTW"


class LoanStatus:
    closed = "closed"
    info_stopped = "info_transfer_stopped"
    active_wo_overdue = "active_wo_overdue"
    active_w_overdue = "active_w_overdue"


COLS = ChqCols
PMT_STATUSES = PaymentDisciplineSymbols
LOAN_STATUSES = LoanStatus


def clear_pmt_line(line: str) -> str:
    if (not line) or pd.isnull(line):
        return ""

    line = re.sub("[-]+", "", line)

    for status in PMT_STATUSES.FINAL:
        line = re.sub(f"^[{status}-]+", f"{status}", line.upper())

    return line


def weights_by_loan_type_and_state(
    d: pd.DataFrame, microloans_only: bool = False
) -> pd.Series:
    microloans = (d[COLS.deal_type] == "microloan") | (
        (d[COLS.partner_type] == "microfinance_organization")
        & ((d[COLS.deal_type] == "another") | (d[COLS.deal_type] == "syndicated_loan"))
    )

    active_wo_overdue = d[COLS.loan_status] == LOAN_STATUSES.active_wo_overdue
    closed = d[COLS.loan_status] == LOAN_STATUSES.closed
    active_w_overdue = d[COLS.loan_status] == LOAN_STATUSES.active_w_overdue
    finished_badly = (
        d[COLS.payment_discipline_cleansed]
        .str.translate(str.maketrans({ch: "_" for ch in PMT_STATUSES.FINAL_W_OVERDUE}))
        .str.contains("_")
    )

    choices = {
        4: microloans & active_wo_overdue,
        5: microloans & closed,
        10: microloans
        & (active_w_overdue | (finished_badly & ~closed & ~active_wo_overdue)),
    }
    if not microloans_only:
        choices.update(
            {
                1: ~microloans & (active_wo_overdue | closed),
                3: ~microloans
                & (active_w_overdue | (finished_badly & ~closed & ~active_wo_overdue)),
            }
        )

    loan_weights = pd.Series(
        np.select(list(choices.values()), list(choices.keys())),
        index=d.index,
        name="loan_weights",
        dtype="float64",
    ).fillna(0)

    return loan_weights


def loan_age_in_months(s: pd.Series) -> int:
    if s[COLS.loan_status] in {
        LOAN_STATUSES.active_wo_overdue,
        LOAN_STATUSES.active_w_overdue,
    }:
        return 0

    else:
        last_date = s[COLS.date_of_factual_closure] or s[COLS.loan_relevance_date]
        dates_are_not_none = pd.notnull(s[COLS.ch_relevance_date]) and pd.notnull(
            last_date
        )

        return (
            relativedelta(s[COLS.ch_relevance_date], last_date).months
            if dates_are_not_none
            else 2
        )


def specific_mean_overdue_by_ovd_line(line: str) -> float:
    def calc_summand(ndx: int, pmt_cat_symbol: str) -> int:
        return (num_of_payments - (ndx + 1) + 1) * (
            int(pmt_cat_symbol) if pmt_cat_symbol.isdigit() else 0
        )

    line_ = re.sub("[CU-]+", "", line)

    num_of_payments = len(line_)

    line_ = re.sub(f"[A{PMT_STATUSES.FINAL_W_OVERDUE}]", "10", line_)

    return (
        (
            (2.0 / (num_of_payments * (num_of_payments + 1)))
            * sum([calc_summand(ndx, symbol) for ndx, symbol in enumerate(line_)])
        )
        if num_of_payments > 0
        else np.nan
    )


def chq(d: pd.DataFrame, microloans_only: bool, col: str) -> pd.DataFrame:
    d[COLS.payment_discipline_cleansed] = (
        d[COLS.payment_discipline].astype(str).apply(clear_pmt_line)
    )

    loan_weights = weights_by_loan_type_and_state(d, microloans_only=microloans_only)

    loan_ages = d.apply(loan_age_in_months, axis=1)

    loan_arrears = d[COLS.payment_discipline_cleansed].apply(
        specific_mean_overdue_by_ovd_line
    )

    if (loan_weights.sum() == 0) or all(loan_arrears.isna()):
        d[col] = np.nan
        return d

    numerator = (loan_weights * loan_arrears / (loan_ages + 1) ** (1 / 2)).sum()
    normalizing_denominator = (loan_weights / (loan_ages + 1) ** (1 / 2)).sum()

    d[col] = (
        numerator / normalizing_denominator if normalizing_denominator > 0 else np.nan
    )

    return d
