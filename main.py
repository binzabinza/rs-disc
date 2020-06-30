from forum_service import ForumService
from db_manager import DBManager
from Models.forum_post_model import ForumPostModel

#initialize our classes
db = DBManager(debugging=True)
fs = ForumService()

#track new threads
url1 = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561,goto,{}"
db.track_new_thread(url1)

# url2 = "https://services.runescape.com/m=forum/sl=0/forums?17,18,769,66133050,goto,{}"
# db.track_new_thread(url2)

#lets try pulling down all the info in both threads
active_threads = db.fetch_active_threads()
total_reports = []
for url, last_page_num, last_post_num, thread_id in active_threads:
   data = fs.get_forum_posts(url, thread_id, 1)

   #let's try inserting each post
   #print(db.insert_forum_post(data))
   #and lets print the price reports from it
   total_reports += fs.get_price_reports(data)

for rep in total_reports:
   print(",".join(rep))
#and let's try extracting the info and printing it to the console
# data = db.fetch_forum_posts(1, 10)
# for dat in data:
#    # print(len(dat), dat)
#    print(ForumPostModel.from_array(dat))

# data = db.fetch_forum_posts(2)
# for dat in data:
#    print(ForumPostModel.from_array(dat))