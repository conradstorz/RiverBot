from datetime import *
from dateutil.parser import *
import pytz

TODAY = date.today()
tz_UTC = pytz.timezone('UTC')
NOW = datetime.now(tz_UTC)
CURRENT_YEAR = TODAY.year
TODAY_STRING = TODAY.strftime("%Y-%m-%d")
NOW_STRING = f'{NOW.strftime("%Y-%m-%d,%H:%M:%S")}UTC'