### Keno DataVis CONFIG ###
## How to read config ##
# Setting = "Default" ### Defualt || Options | Recommended | Description
from keno import keno_app

### COFNIG CHECK, DISABLING THE CHECK CAN CAUSE THE PROGRAM TO BREAK. It is best to leave it on unless you know what your doing\
Config_Check = True ### True || True / False | Keep as True | Checks config for invaild values

ConfigVersion = "v0.1.d-23"
app = keno_app.KenoAPI("VIC") ### VIC || VIC NSW (TAS, NT, SA, WA) -> ACT QLD | your state | State the data comes from
cooldown = 160 ### 160 || <140 to inf> | around 160 | Time between Auto API calls
countdown = "True" ### "True" || "True"/"False"/"Manual" | n/a |Turn off/on the countdown or press [Enter] to request API again