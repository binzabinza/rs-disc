import requests
from lxml import html
from typing import List, Tuple

import time

class RSScraper:
    """
        Handles interaction with the forum and parsing html.
    """

    def __init__(self, thread_url: str):
        """
        Initializes an RSScraper object.

        Parameters
        ----------
        thread_url : str
            The url of the forum thread that this RSScraper instance will scrape.
        """
        self.thread_url = thread_url  #url of the thread to be scraped

    def __create_tree(self, page_num: int, tries_left: int = 10):
        """
        Creates a tree object for XPath queries and saves it to self.current_tree.

        Parameters
        ----------
        page_num : int
            The page of the forum thread to create the tree for.
        tries_left : int
            The number of tries remaining. This is the number of times the method
            will recurse to retry the http request if it fails initially.
            Defaults to 10.
        """
        if tries_left <= 0:
            print(f'ERROR: Failed to create tree for html on page {page_num}')
            return None

        response = requests.get(
            self.thread_url.format(page_num),
            headers={'content-type' : 'application/json'}
        )

        if response.status_code != 200:
            time.sleep(0.25)
            self.__create_tree(page_num, tries_left=tries_left-1)

        return html.fromstring(response.content)

    def scrape_page(self, page_index: int, post_index_start: int = 1) -> List[Tuple[str, str, str, int, int]]:
        """
        Scrape content off of the page specified by page_index.

        NOTE: by default this method will return the entire page. By passing a post_index_start, it will return less!!!

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
        tree = self.__create_tree(page_index)
        usernames = self.__scrape_usernames(tree)
        num_posts = self.__get_num_posts(tree)

        timestamps = []
        bodies     = []
        post_nums  = [x for x in range(post_index_start, num_posts + 1)]
        page_nums  = [page_index] * len(post_nums)

        for i in range(post_index_start, num_posts + 1): #1 based indexing because dumb
            bodies.append(self.__scrape_posts(i, tree))
            timestamps.append(self.__scrape_timestamps(i, tree))
        
        #check for deleted posts
        for i, post in enumerate(bodies):
            if post == 'The contents of this message have been hidden':
                usernames.insert(i, None)
        return list(zip(timestamps, usernames, bodies, post_nums, page_nums))

    ################################
    #  This section contains all scraping methods. All XPath querys appear here
    ###############################
    def __get_num_posts(self, tree) -> int:
        """ Counts the number of posts (article nodes) on a given page. """
        cnt = tree.xpath('count(//article)')
        return int(cnt)

    def __scrape_usernames(self, tree) -> str:
        usernames_raw = tree.xpath('//a[@class="post-avatar__name-link"]//text()')
        usernames = list([x.encode('ascii', 'ignore').decode('ascii') for x in usernames_raw])  # don't touch this it will super fuck usernames up
        return usernames

    def __scrape_posts(self, post_num: int, tree) -> str:
        post_raw  = tree.xpath(f'//article[{post_num}]//span[@class="forum-post__body"]//text()')
        post_text = "\n".join(post_raw)
        return post_text

    def __scrape_timestamps(self, post_num: int, tree) -> str:
        timestamp_raw = tree.xpath(f'//article[{post_num}]//p[@class="forum-post__time-below"]//text()')
        timestamp_text = " ".join(timestamp_raw)
        return timestamp_text

    def get_max_page(self) -> int:
        """
        Determines the total number of pages on the thread.

        Returns
        -------
        int
            The page number of the last page of this thread.
        """
        tree = self.__create_tree(1)
        return int(tree.xpath('//a[@class="forum-pagination__top-last"]//text()')[0])
