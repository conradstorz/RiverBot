from datetime import *
from dateutil.parser import *
import pytz

TODAY = date.today()
tz_UTC = pytz.timezone("UTC")


def timefstring(dtobj):
    return f'{dtobj.strftime("%Y-%m-%d_%H:%M:%S")}UTC'


NOW = datetime.now(tz_UTC)
CURRENT_YEAR = TODAY.year
TODAY_STRING = TODAY.strftime("%Y-%m-%d")
NOW_STRING = timefstring(NOW)

if __name__ == "__main__":
    print(f"TODAY: {TODAY} type: {type(TODAY)}")
    print(f"NOW: {NOW} type: {type(NOW)}")
    print(f"CURRENT_YEAR: {CURRENT_YEAR} type: {type(CURRENT_YEAR)}")
    print(f"TODAY_STRING: {TODAY_STRING} type: {type(TODAY_STRING)}")
    print(f"NOW_STRING: {NOW_STRING} type: {type(NOW_STRING)}")
