# Credit history Quality Score

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
