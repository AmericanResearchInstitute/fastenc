# Example GetMediaList call
from fastenc.actions import GetMediaList
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

userid = 0000
userkey = 'youruserkey'

action = GetMediaList(userid, userkey)

res = action.send()
