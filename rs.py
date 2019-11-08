import requests
from lxml import html


url = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561"

page = requests.get(url, headers={'content-type' : 'application/json'})
tree = html.fromstring(page.content)

message_content = tree.xpath('//span[@class="forum-post__body]/text()"]')
print message_content
