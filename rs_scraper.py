import requests, sqlite3
from lxml import html

class RS_Scraper:
    def __init__(self, thread):
        #initialize scraping object
        self.thread = thread
        self.timestamps = []
        self.bodies     = []
        self.usernames  = []

        tmp = self.create_tree(thread) #here2
        self.current_page = self.get_current_page(tmp)
        self.max_page     = self.get_max_page(tmp)

    def __str__(self):
        #prints formatted content scraped from page
        text = ""
        for i, timestamp in enumerate(self.timestamps):
            if self.usernames[i] is None :
                text +=  "\n"
            else :
                text += self.usernames[i] + "\n"
            # text += "" + "\n" if self.usernames[i] is None else text += self.usernames[i] + "\n"
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

        self.scrape_usernames(tree)
        num_posts = self.get_num_posts(tree)

        for i in range(1, num_posts + 1): #1 based indexing because dumb
            self.scrape_posts(tree, i)
            self.scrape_timestamps(tree, i)

    ################################
    #  This section contains all scraping methods. All XPath querys appear here
    ###############################
    def get_num_posts(self, tree):
        #counts the number of posts (article nodes) on a given page
        cnt = tree.xpath('count(//article)')
        return int(cnt)

    def scrape_usernames(self, tree):
        usernames_raw = tree.xpath('//a[@class="post-avatar__name-link"]//text()')
        usernames = list([x.encode('ascii', 'ignore').decode('ascii') for x in usernames_raw])  # don't touch this it will super fuck usernames up
        self.usernames += usernames

    def scrape_posts(self, tree, post_num):
        post_raw  = tree.xpath(f'//article[{post_num}]//span[@class="forum-post__body"]//text()')
        post_text = "\n".join(post_raw)
        self.bodies.append(post_text)

    def scrape_timestamps(self, tree, post_num):
        timestamp_raw = tree.xpath(f'//article[{post_num}]//p[@class="forum-post__time-below"]//text()')
        timestamp_text = " ".join(timestamp_raw)
        self.timestamps.append(timestamp_text)

    def get_max_page(self, tree):
        # Determines the total number of pages on the thread
        # Takes an HTML tree object. Sets and returns the object variable max_page
        maxp = int(tree.xpath('//a[@class="forum-pagination__top-last"]//text()')[0])
        self.max_page = maxp
        return self.max_page

    def get_current_page(self, tree):
        # Determines the current page number in the thread
        # Takes an HTML object. Sets and retunrs the object variable current_page
        curp = int(tree.xpath('//li[@class="current"]/a/text()')[0])
        self.current_page = curp
        return self.current_page

    ###################
    # Miscellaneous Methods
    ###################
    def store_last_timestamp(self, url, filename="last_scraped_post.txt"):
        # this will save the latest timestamp in the cache to a file
        last_timestamp = self.timestamps[-1]
        f = open(filename, 'w')
        f.write(url)
        f.write('\n')
        f.write(str(self.current_page))
        f.write('\n')
        f.write(last_timestamp)
        f.close()
        return last_timestamp

    def save_cache(self):
        #TODO: method of saving what has been scraped
        #right now we are simply dumping the object to terminal
        conn = sqlite3.connect('rs-forum.db')
        c = conn.cursor()
        #INSERT statement here
        conn.exit()
        print(self)

    def clear_cache(self):
        #this will reset the (cache|buffer) object variables
        self.timestamps = []
        self.bodies     = []
        self.usernames  = []

    def check_deleted(self):
        #checks for deleted posts and inserts None into corresponding usernames list
        for i, post in enumerate(self.bodies):
            if post == 'The contents of this message have been hidden':
                self.usernames.insert(i, None)

##########
# main debugging
##########
url = "http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561,goto,{}"

s = RS_Scraper(url) #erroring here

# !!CURRENT ISSUE !!! 11/20 1:55AM CT
# The following page:
#       http://services.runescape.com/m=forum/forums.ws?17,18,812,66119561,goto,29
# contains a post that has been (deleted|hidden) and as such, no username is associated
# This needs to be remedied
#!!!!!

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
