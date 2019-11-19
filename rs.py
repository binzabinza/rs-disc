import requests
from lxml import html

class RS_Scraper:
    def __init__(self, n=10):
        #initialize scraping object
        self.n          = n  #unused
        self.timestamps = []
        self.bodies     = []
        self.usernames  = []

    def __str__(self):
        #prints formatted content scraped from page
        text = ""
        for i, timestamp in enumerate(self.timestamps):
            # text += self.usernames[i] + "\n"
            text += self.bodies[i] + " \n"
            text += timestamp +"\n"
            text += "---\n"
        return text

    def create_tree(self, stream, format='url'):
        #creates a tree object for XPath queries. can be created from an HTML file or a webpage url
        #
        #     inputs  :  type  : required  :  default  :  possible values
        #     stream  :  str   :    yes    :           :
        #     format  :  str   :           :  'url'    : 'url', 'file'
        #
        if (format == 'url'):
            page = requests.get(stream, headers={'content-type' : 'application/json'})
            tree = html.fromstring(page.content)
        elif (format == 'file'):
            #TODO: lxml library probably has a way to this
            with open(stream, 'r') as f:
                page = f.read()
            tree = html.fromstring(page)
        return tree

    def scrape(self, tree):
        #scrape content off of html tree
        #
        #     inputs  :     type     : required  :  default  :  possible values
        #     tree    :  lxml.tree   :    yes    :           :
        #
        #This will error for the last page where there are <=10 posts
        for i in range(1,11): #TODO: find a simple way to determine how many posts are on a page.
            #grab content from html tree using XPath Query
            #TODO: grab usernames
            #usernames_raw = tree.xpath('//h3[@class="post-avatar__name"]/@data-displayname"]') #TODO: not working!
            post_raw      = tree.xpath(f'//article[{i}]//span[@class="forum-post__body"]//text()')
            timestamp_raw = tree.xpath(f'//article[{i}]//p[@class="forum-post__time-below"]//text()')

            #cleanup data into readable format
            post_text = "\n".join(post_raw)
            timestamp_text = " ".join(timestamp_raw)

            #add to object attributes
            self.bodies.append(post_text)
            self.timestamps.append(timestamp_text)

    def store_last_timestamp(self):
        #TODO: store the last scraped timestamp
        pass

    def save_cache(self):
        #TODO: method of saving what has been scraped
        pass

    def clear_cache(self):
        #this will reset the object
        #probably should be deprecated and roll into save_cache
        self.__init__()



##########
# main debugging
##########
url = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561,goto,{}"

s = RS_Scraper()

for i in range(1, 3):
    x = s.create_tree(url.format(i))
    s.scrape(x)

print(s)
