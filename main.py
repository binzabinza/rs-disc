from forum_service import ForumService
from rs_cleaner import RSCleaner
from db_manager import DBManager

url1 = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561,goto,{}"
# url2 = "https://secure.runescape.com/m=forum/sl=0/forums?17,18,769,66133050,goto,{}"

fs = ForumService()
print(fs.get_raw_posts(url1, 1, 2))