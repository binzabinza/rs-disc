import requests
from lxml import html
from typing import List, Tuple

class RSScraper:
    """
        Handles interaction with the forum and parsing html.
    """

    def __init__(self, thread_url: str):
        #initialize scraping object
        self.thread_url = thread_url  #url of the thread to be scraped

        self.__create_tree__("")
        self.max_page     = self.get_max_page()
        self.current_page = self.get_current_page() #number corresponding to current page
        self.current_post = 1  #post number on the current page, defaults to 1

    def __str__(self) -> str:
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

    def __create_tree__(self, page_num: int):
        """
        Creates a tree object for XPath queries and saves it to self.current_tree.

        Parameters
        ----------
        page_num : int
            The page of the forum thread to create the tree for.
        """
        page = requests.get(self.thread_url.format(page_num), headers={'content-type' : 'application/json'})
        tree = html.fromstring(page.content)
        self.current_tree = tree

    def scrape_page(self, page_index: int, post_index_start: int = 1) -> List[Tuple[str, str, str, int, int]]:
        """
        Scrape content off of the page specified by page_index.

        NOTE: by deafault this method will return the entire page. By passing a post_index_start, it will return less!!!

        Parameters
        ----------
        page_index : int
            The page of the forum thread that should be scraped.

        post_index_start : int
            The index of the first post on the page to start scraping from (1-indexed). Defaults to first post on page.

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
        post_nums  = [x for x in range(post_index_start, num_posts + 1)]
        page_nums  = [self.current_page] * len(post_nums)

        for i in range(post_index_start, num_posts + 1): #1 based indexing because dumb
            bodies.append(self.scrape_posts(i))
            timestamps.append(self.scrape_timestamps(i))
            self.current_post = i
        
        #check for deleted posts
        for i, post in enumerate(bodies):
            if post == 'The contents of this message have been hidden':
                usernames.insert(i, None)
        return list(zip(timestamps, usernames, bodies, post_nums, page_nums))

    ################################
    #  This section contains all scraping methods. All XPath querys appear here
    ###############################
    def get_num_posts(self) -> int:
        #counts the number of posts (article nodes) on a given page
        cnt = self.current_tree.xpath('count(//article)')
        return int(cnt)

    def scrape_usernames(self) -> str:
        usernames_raw = self.current_tree.xpath('//a[@class="post-avatar__name-link"]//text()')
        usernames = list([x.encode('ascii', 'ignore').decode('ascii') for x in usernames_raw])  # don't touch this it will super fuck usernames up
        return usernames

    def scrape_posts(self, post_num: int) -> str:
        post_raw  = self.current_tree.xpath(f'//article[{post_num}]//span[@class="forum-post__body"]//text()')
        post_text = "\n".join(post_raw)
        return post_text

    def scrape_timestamps(self, post_num: int) -> str:
        timestamp_raw = self.current_tree.xpath(f'//article[{post_num}]//p[@class="forum-post__time-below"]//text()')
        timestamp_text = " ".join(timestamp_raw)
        return timestamp_text

    def get_max_page(self) -> int:
        # Determines the total number of pages on the thread
        # Takes an HTML tree object. Sets and returns the object variable max_page
        maxp = int(self.current_tree.xpath('//a[@class="forum-pagination__top-last"]//text()')[0])
        self.max_page = maxp
        return self.max_page

    def get_current_page(self) -> int:
        # Determines the current page number in the thread
        # Takes an HTML object. Sets and retunrs the object variable current_page
        curp = int(self.current_tree.xpath('//li[@class="current"]/a/text()')[0])
        self.current_page = curp
        return self.current_page