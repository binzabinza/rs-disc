from forum_service import ForumService
from db_manager import DBManager
from Models.forum_post_model import ForumPostModel

from time import time

#initialize our classes
db = DBManager(debugging=True)

#track new threads
#url1 = "https://secure.runescape.com/m=forum/a=23/c=Yaws3WNAKrQ/forums?17,18,741,66165612,goto,{}"
url1 = "https://secure.runescape.com/m=forum/a=23/c=Yaws3WNAKrQ/forums?17,18,398,66147587,goto,{}"
db.track_new_thread(url1)

# url2 = "https://services.runescape.com/m=forum/sl=0/forums?17,18,769,66133050,goto,{}"
# db.track_new_thread(url2)

#lets try pulling down all the info in both threads
active_threads = db.fetch_active_threads()
total_reports = []
total_posts = []
for url, last_page_num, last_post_num, thread_id in active_threads:
    forum_service = ForumService(url)

    print(f'fetching posts from forum -- {thread_id}\n  url: {url}')

    start = time()
    #posts, price_reports = forum_service.get_forum_posts_and_reports(thread_id, 1, 60)
    posts, price_reports = forum_service.get_forum_posts_and_reports(thread_id, 1)
    print(f'posts: {len(posts)}, price reports: {len(price_reports)}')
    print(f'runtime: {time() - start}\n')


    #let's try inserting each post
    #print(db.insert_forum_post(data))
    #and lets print the price reports from it
    #total_reports += forum_service.get_price_reports(posts)

    total_reports += price_reports
    total_posts += posts

csv = ''
for rep in total_reports:
    csv_string = '{page}, {post}, {time}, {type_}, {item_id}, {price}\n'.format(
        page = rep.page_id,
        post = rep.post_id,
        time = rep.time,
        type_ = rep.transaction_type,
        item_id = rep.item_id,
        price = rep.price
    )
    #print(csv_string)
    csv += csv_string

# write to output file
with open('output.csv', 'w') as f:
    f.write(csv)


posts = ''
for post in total_posts:
    body = post.post_body.replace(',', '<...>').replace('\r', '---'.replace('\n', '---'))
    posts += f'{post.timestamp}, {post.thread_id}, {post.page_num}, {post.post_num}, {body}\n'

with open('posts.csv', 'w') as f:
    f.write(posts)

    

#and let's try extracting the info and printing it to the console
# data = db.fetch_forum_posts(1, 10)
# for dat in data:
#    # print(len(dat), dat)
#    print(ForumPostModel.from_array(dat))

# data = db.fetch_forum_posts(2)
# for dat in data:
#    print(ForumPostModel.from_array(dat))
