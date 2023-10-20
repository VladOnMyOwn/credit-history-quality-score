import pandas as pd
from chq import chq

data_path = "path\\to\\data\\"
save_path = "path\\to\\save\\chq\\"

if __name__ == "__main__":
    data = pd.read_feather(data_path)

    columns_to_calc = [
        "ApplicationDate",
        "DealUID",
        "PaymentDiscipline",
        "LoanKindCode",
        "BCHPartnerType",
        "CreditStatus",
        "CloseDtFact",
        "LastUpdateDt",
    ]

    data_w_chq = data.groupby(by="ApplicationID")[columns_to_calc].apply(
        chq, microloans_only=False, col="chq"
    )

    agg_chq = {"chq": lambda s: s.values[0]}
    data_collapsed = data_w_chq.groupby(by="ApplicationID").agg(agg_chq)

    data_collapsed.to_feather(save_path)
