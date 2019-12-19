import requests, sqlite3
from lxml import html

class RSScraper:

    def __init__(self, thread):
        #initialize scraping object
        self.thread = thread  #url of the thread to be scraped

        self.__create_tree__("") #create a tree and set it to current page
        self.max_page     = self.get_max_page()     #total number of pages in the thread
        self.current_page = self.get_current_page() #number corresponding to current page
        self.current_post = 1  #post number on the current page, defaults to 1

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

    def __create_tree__(self, page_num):
        """
        creates a tree object for XPath queries and saves it to self.current_tree
            inputs   :  type  : required  :  default  :  possible values
            page_num : int    : yes       :           :
        """
        page = requests.get(self.thread.format(page_num), headers={'content-type' : 'application/json'})
        tree = html.fromstring(page.content)
        self.current_tree = tree

    def scrape_page(self, page_index, post_index=1):
        """
        !!!NOTE: by deaful this method will return the entire page. By passing a page_index, it will return less!!!!
        
        Scrape content off of the page specified by page_index

        Parameters
        ----------
        page_index : int
            The page of the forum thread that should be scraped.

            Returns
            -------
            list
                A list of tuples containing the timestamps, usernames, and bodies of the posts on the requested pages.
        """
        self.current_page = page_index
        self.__create_tree__(page_index)
        usernames = self.scrape_usernames()
        num_posts = self.get_num_posts()

        timestamps = []
        bodies     = []
        for i in range(1, num_posts + 1): #1 based indexing because dumb
            bodies.append(self.scrape_posts(i))
            timestamps.append(self.scrape_timestamps(i))
            self.current_post = i
        
        #check for deleted posts
        for i, post in enumerate(bodies):
            if post == 'The contents of this message have been hidden':
                usernames.insert(i, None)
        return list(zip(timestamps, usernames, bodies))

    ################################
    #  This section contains all scraping methods. All XPath querys appear here
    ###############################
    def get_num_posts(self):
        #counts the number of posts (article nodes) on a given page
        cnt = self.current_tree.xpath('count(//article)')
        return int(cnt)

    def scrape_usernames(self):
        usernames_raw = self.current_tree.xpath('//a[@class="post-avatar__name-link"]//text()')
        usernames = list([x.encode('ascii', 'ignore').decode('ascii') for x in usernames_raw])  # don't touch this it will super fuck usernames up
        return usernames

    def scrape_posts(self, post_num):
        post_raw  = self.current_tree.xpath(f'//article[{post_num}]//span[@class="forum-post__body"]//text()')
        post_text = "\n".join(post_raw)
        return post_text

    def scrape_timestamps(self, post_num):
        timestamp_raw = self.current_tree.xpath(f'//article[{post_num}]//p[@class="forum-post__time-below"]//text()')
        timestamp_text = " ".join(timestamp_raw)
        return timestamp_text

    def get_max_page(self):
        # Determines the total number of pages on the thread
        # Takes an HTML tree object. Sets and returns the object variable max_page
        maxp = int(self.current_tree.xpath('//a[@class="forum-pagination__top-last"]//text()')[0])
        self.max_page = maxp
        return self.max_page

    def get_current_page(self):
        # Determines the current page number in the thread
        # Takes an HTML object. Sets and retunrs the object variable current_page
        curp = int(self.current_tree.xpath('//li[@class="current"]/a/text()')[0])
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