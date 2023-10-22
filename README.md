# Credit history Quality Score

The attribute «credit history quality» (CHQ) is calculated as the weighted categorized average of the client’s delay and is a variant of the assessment of solvency calculated for all loans of the client.  
This average depends on a number of attributes: the date of validity of the loan, the type of loan, the dynamics of payments / arrears for each of the loans. Obviously, recent microloans are many times more important and interesting than two-year consumer loans: all this is taken into account in the feature calculation formula.  
We will use the «Payment discipline» credit history (CH) attribute to calculate the CHQ feature value. This attribute contains information about the timeliness of payments under the loan or loan agreement. The attribute value is a string consisting of a number of digits (symbols), with the leftmost symbol corresponding to the month of the date on which the credit report (CR) was requested. If you move one bit to the right, you get a value for the previous month; if you move two bits to the right, a value that was two months ago and so on.

Values of "Payment Discipline" attribute bits:
| Contract Status                        | BCH Designation | Designation Used for Feature Calculation            |
| ------------------------------------- | ----------------------- | --------------------------------------------------- |
| No data                               | -                       | Not used in calculation                             |
| No delay                        | 0                       | 0                                                 |
| Delay 1-5 days                  | 1                       | 1                                                 |
| Delay 6-29 days                 | 2                       | 2                                                 |
| Delay 30-59 days                | 3                       | 3                                                 |
| Delay 80-89 days                | 4                       | 4                                                 |
| Delay 90-119 days               | 5                       | 5                                                 |
| Delay 120-149 days              | 6                       | 6                                                 |
| Delay 150-179 days              | 7                       | 7                                                 |
| Delay 180-209 days              | 8                       | 8                                                 |
| Delay 210-239 days              | 9                       | 9                                                 |
| Delay >= 240 days               | A                       | 10                                                |
| Hopeless debt (written off)           | B                       | 10                                                |
| Contract closed                       | C                       | Not used in calculation                             |
| Contract sold (assignment of rights)  | S                       | 10                                                |
| Contract restructured / refinanced    | R                       | 10                                                |
| Contract sold to collectors           | W                       | 10                                                |
| Contract terminated                   | U                       | Not used in calculation                             |
| Subject of CH declared bankrupt       | T                       | 10                                                |
| Information transmission ceased | I                       | 10                                                |

Feature calculation formula is as follows:  
$CHQ=\frac{1}{W} \sum_{i=1}^{n} \frac{wt_i}{\sqrt{M_i + 1}}\cdot D_i$,  
where $n$ is the total number of loans in the customer’s credit history, $M_i$ is the number of full months from the current date to the closing date or, if the latter is absent, the date of the last update of the information about the $i$-th commitment in the borrower’s credit history,  
$W=\sum_{i=1}^{n} \frac{wt_i}{\sqrt{M_i + 1}}$ is the normalizing ratio, $wt_i$ is a corrective factor depending on the type of $i$-th loan.  
Note that the optimum values of the corrective coefficients can be found in some neighborhood of the values given in table below by optimizing some target function, e.g. maximizing the value of information value (IV) of the considering feature or the Gini metric value of the model in which this feature is planned to be included.  

Values of correction coefficients of credit type:
| Credit Obligation Type     | Current Contract Status     | Weight ($wt_i$) |
| -------------------------- | --------------------------- | ------------ |
| Microloan                  | Closed                      | 5            |
|                            | Active with no current overdue | 4  |
|                            | "Payment discipline" contract Status: B, S, R, W, T, I | 10 |
|                            | Active with current overdue | 10 |
| Other                      | Closed                      | 1            |
|                            | Active with no current overdue | 1  |
|                            | Active with current overdue | 3  |
|                            | "Payment discipline" contract Status: B, S, R, W, T, I | 3  |

The value of the term $D_i$ is calculated using the following formula:  
$D_i=\frac{2}{P_i*(P_i+1)}\sum_{k=1}^{P_i}(P_i - k + 1)\cdot d_{ik}$,  
where $d_{ik}$ is the k-th payment overdue category number of the 1st loan.  
The value of the term, calculated in an expression above, is a weighted delay of payments on a specific loan obligation of the borrower.  
We have the correspondence of the categories of delay, presented in the last column of table 1. It is not difficult to conclude that the values of the feature vary from 0 to 10.  
Note also that payments in the «Payment discipline» line of the credit are numbered from left to right: from the newest on the date of payment ($k=1$) to the oldest ($k=P_i$). Thus, the most relevant payments/delays will have higher weight in calculating the value of the member.

The input to the script must be a processed pandas dataframe with the fields of the credit report necessary for calculating the feature values. The list of such fields contains:
- internal unique identifier of the client (borrower);
- “Payment discipline” line;
- code of the loan type, specific to the format of the credit report of each specific bank;
- type of credit bureau partner with whom the borrower opened a loan obligation;
- status of the contract of obligation at the current moment;
- actual date of closing of the loan agreement;
- internal date of the loan application;
- date of the last change in the entry on the credit obligation in the credit report;
- unique universal transaction identifier.
