### Keno DataVis CONFIG ###
## How to read config ##
# Setting = "Default" ### Defualt || Options | Recommended | Description
from keno import keno_app

### COFNIG CHECK, DISABLING THE CHECK CAN CAUSE THE PROGRAM TO BREAK. It is best to leave it on unless you know what your doing\
configCheck = True ### True || True / False | Keep as True | Checks config for invaild values

configVersion = "Legacy-08/2023-1"
app = keno_app.KenoAPI("VIC") ### VIC || VIC NSW (TAS, NT, SA, WA) -> ACT QLD | your state | State the data comes from
cooldown = "Auto" ### "Auto" || <140 to inf> or "Auto" | Keep to Auto | Time between Auto API calls
countdown = "True" ### "True" || "True"/"False"/"Manual" | n/a |Turn off/on the countdown or press [Enter] to request API again