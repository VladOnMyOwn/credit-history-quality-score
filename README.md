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
