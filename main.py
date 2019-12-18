from rs_scraper import RS_Scraper

url = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561,goto,{}"

s = RS_Scraper(url)

for i in range(29, 30): #1 based indexing because dumb
    page_tree = s.create_tree(url.format(i))
    s.scrape(page_tree)

    #s.save_cache()
    #if i % 40 != 0 : s.clear_cache()

s.check_deleted()
s.store_last_timestamp(url)
# print(s)
print(s.usernames)
print(s.bodies)
print(s.timestamps)
