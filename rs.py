import requests
from lxml import html


url = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561"

page = requests.get(url, headers={'content-type' : 'application/json'})
print page.content
