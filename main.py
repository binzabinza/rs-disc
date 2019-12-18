from forum_service import ForumService

url = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561,goto,{}"

forum_service = ForumService()


# threads = forum_service.fetch_active_threads()
# for thread in threads:
#     posts       = forum_service.get_price_posts(url, 1, 5)
#     clean_posts = forum_service.clean_posts(posts)
#     forum_service.price_reports_db_insert(clean_posts)
#     forum_service.threads_db_insert(thread_data)

print(forum_service.get_price_posts(url, 1, 5))

# scraper.check_deleted() #NOTE needs to be placed into scraper class

