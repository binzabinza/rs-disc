import requests
from lxml import html


url = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561"

# page = requests.get(url, headers={'content-type' : 'application/json'})

with open(r'page_content.html', 'r') as f:
    page = f.read()
tree = html.fromstring(page)

#it looks like the body's of the post are themselves html. How do I pull out all the elements grouped by post?
#lets try looping over each individual post, creating a subtree everytime. Scrape all text as plain, then concatentate.
# timestamp = tree.xpath('//p[@class="forum-post__time-below"]//text()')
# print(timestamp)

for i in range(1,11):
    post_raw = tree.xpath(f'//article[{i}]//span[@class="forum-post__body"]//text()')
    timestamp = tree.xpath(f'//article[{i}]//p[@class="forum-post__time-below"]//text()')
    post_text = "\n".join(post_raw)
    print(post_text)
    print(timestamp)
    print('\n--END--\n')  # there may be a way to clean all this up
