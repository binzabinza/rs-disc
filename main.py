from forum_service import ForumService
from db_manager import DBManager
from Models.forum_post_model import ForumPostModel

#initialize our classes
db = DBManager()
fs = ForumService()

#track new threads
url1 = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561,goto,{}"
url2 = "https://services.runescape.com/m=forum/sl=0/forums?17,18,769,66133050,goto,{}"
db.track_new_thread(url1)
db.track_new_thread(url2)

#lets try pulling down all the info in both threads
active_threads = db.fetch_active_threads()
for url, last_page_num, last_post_num, thread_id in active_threads:
   data = fs.get_clean_forum_posts(url, thread_id, 1)
   
   #this will create a list of ForumPost objects using the properly cleaned forum post information
   forum_posts = []
   for post in data:
      forum_posts.append(ForumPostModel.from_array(post))

   #let's try inserting each post
   print(db.insert_forum_post(forum_posts))

#and let's try extracting the info and printing it to the console
data = db.fetch_forum_posts(1)
for dat in data:
   print(ForumPostModel.from_array(dat))

data = db.fetch_forum_posts(2)
for dat in data:
   print(ForumPostModel.from_array(dat))