# credit-history-quality-score
The script for calculating the credit history quality of the microfinance organization's borrower. It can be extended to banks' borrowers

Values of "Payment Discipline" attribute bits:
| Contract Status                        | BCH Designation | Designation Used for Feature Calculation            |
| ------------------------------------- | ----------------------- | --------------------------------------------------- |
| No data                               | -                       | Not used in calculation                             |
| No delinquency                        | 0                       | 0                                                 |
| Delinquency 1-5 days                  | 1                       | 1                                                 |
| Delinquency 6-29 days                 | 2                       | 2                                                 |
| Delinquency 30-59 days                | 3                       | 3                                                 |
| Delinquency 80-89 days                | 4                       | 4                                                 |
| Delinquency 90-119 days               | 5                       | 5                                                 |
| Delinquency 120-149 days              | 6                       | 6                                                 |
| Delinquency 150-179 days              | 7                       | 7                                                 |
| Delinquency 180-209 days              | 8                       | 8                                                 |
| Delinquency 210-239 days              | 9                       | 9                                                 |
| Delinquency >= 240 days               | A                       | 10                                                |
| Hopeless debt (written off)           | B                       | 10                                                |
| Contract closed                       | C                       | Not used in calculation                             |
| Contract sold (assignment of rights)  | S                       | 10                                                |
| Contract restructured / refinanced    | R                       | 10                                                |
| Contract sold to collectors           | W                       | 10                                                |
| Contract terminated                   | U                       | Not used in calculation                             |
| Subject of CI declared bankrupt       | T                       | 10                                                |
| Information transmission ceased to CI | I                       | 10                                                |
