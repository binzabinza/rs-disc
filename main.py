from forum_service import ForumService
from post_cleaner import PostCleaner
from db_manager import DBManager

url1 = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561,goto,{}"
url2 = "https://services.runescape.com/m=forum/sl=0/forums?17,18,769,66133050,goto,{}"

fs = ForumService()
db = DBManager()

db.track_new_thread(url1)
db.track_new_thread(url2)

active_threads = db.fetch_active_threads()

for thread in active_threads:
   url, last_page, last_post, thread_id = thread
   data, last_page, last_post = fs.get_raw_posts(url, last_page, last_page + 5)
   db.insert_raw_posts(data, thread_id)
   db.update_tracked_threads(thread_id, last_page, last_post)