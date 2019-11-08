import requests
from lxml import html

# with open(r'page_content.html', 'r') as f:
#     page = f.read()
# tree = html.fromstring(page)

class RS_Scraper:
    def __init__(self, n=10):
        #initialize scraping object
        self.n          = n
        self.timestamps = []
        self.bodies     = []
        self.usernames  = []

    def __str__(self):
        #prints formatted content scraped from page
        text = ""
        for timestamp in len(timestamps):
            text += self.usernames[i] + "\n"
            text += self.bodies[i] + " \n"
            text += self.usernames[i] +"\n"
            text += "---"
        return text

    def scrape(self, url):
        page = requests.get(url, headers={'content-type' : 'application/json'})
        tree = html.fromstring(page.content)
        for i in range(1,11):
            #grab content from html tree using XPath Query
            post_raw = tree.xpath(f'//article[{i}]//span[@class="forum-post__body"]//text()')
            timestamp_raw = tree.xpath(f'//article[{i}]//p[@class="forum-post__time-below"]//text()')

            #cleanup data into readable format
            post_text = "\n".join(post_raw)
            timestamp_text = " ".join(timestamp_raw)

            #add to object attributes
            self.bodies.append(post_text)
            self.timestamps.append(timestamp_text)




##########
# main debugging
##########

url = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561"
