### Keno DataVis CONFIG ###
## How to read config ##
# Setting = "Default" ### Defualt || Options | Recommended | Description
from keno import keno_app

ConfigVersion = "v0.1.d-18"
app = keno_app.KenoAPI("VIC") ### VIC || VIC NSW (TAS, NT, SA, WA) -> ACT QLD | your state | State the data comes from
cooldown = 180 ### 180 || <0 to 200> | anything around 2.5 to 3 minutes | Time between Auto API calls
countdown = "True" ### "True" || "True"/"False"/"Manual" | n/a |Turn off/on the countdown or press [Enter] to request API again