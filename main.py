from forum_service import ForumService
from post_cleaner import PostCleaner
from db_manager import DBManager

db = DBManager()

# url1 = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561,goto,{}"
# url2 = "https://services.runescape.com/m=forum/sl=0/forums?17,18,769,66133050,goto,{}"
# db.track_new_thread(url1)
# db.track_new_thread(url2)

active_threads = db.fetch_active_threads()

fs = ForumService()

for url, last_page, last_post, thread_id in active_threads:
   data, last_page, last_post = fs.get_raw_posts(url, 1, 3)
   db.insert_many_raw_posts(data, thread_id)
   db.update_tracked_threads(thread_id, last_page, last_post)


   # scrape_data -> dump data to raw_posts
   # grab from raw_posts -> clean it -> dump to price_reports
   #
   # scrape_data -> dump data to raw_posts, also clean data -> dump to price_reports
