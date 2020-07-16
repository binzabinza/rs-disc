from rs_scraper import RSScraper
from post_cleaner import PostCleaner
from datetime import datetime as dt
from typing import List, Tuple
from Models.forum_post_model import ForumPostModel
from Models.price_report_model import PriceReportModel

from concurrent.futures import ThreadPoolExecutor, as_completed

class ForumService:
    """
        Handles the scraping calls and cleaning data
    """


    def __init__(self, url):
        self.url = url
        self.scraper = RSScraper(url)

    def get_forum_posts_and_reports(self, 
        thread_id: str, 
        page_start: int, 
        page_end: int = 0
    ) -> Tuple[List[ForumPostModel], List[PriceReportModel]]:
        """
            Takes a url, thread_id, page_start, and optionally, a page_end
            it will return a list of ForumPostModel objects containing properly formatted forum post information
            for the specified page range. defaults to last page if a specific page is not specified
        """
        if (not page_end) : page_end = RSScraper(self.url).get_max_page() + 1 #NOTE: is this bad practice??

        processes = []
        with ThreadPoolExecutor(max_workers=48) as executor:
            for page_index in range(page_start, page_end):
                processes.append(executor.submit(self.get_forum_posts_on_page, thread_id, page_index))

        posts = []
        for process in as_completed(processes):
            posts += process.result()

        price_reports = []
        for post in posts:
            price_reports += PostCleaner.extract_price_reports(post = post)

        return (posts, price_reports)

    def get_forum_posts_on_page(self,
            thread_id: str, 
            page_num: int
        ) -> List[ForumPostModel]:
        """
        Gets the forum posts found on a specified page number.

        Parameters
        ----------
        thread_id : str
            A unique ID for the thread this `ForumService` object is responsible for.

        Returns
        -------
        List[ForumPostModel]
            A list of `ForumPostModel` objects.
        """

        raw_posts = self.scraper.scrape_page(page_num)
        scraped_time = str(dt.now())

        return PostCleaner.prepare_forum_data(raw_posts, thread_id, scraped_time)
    
    def __get_raw_forum_post__(self, url, page_num):
        """
            Takes a url and a page_num
            returns a list of uncleaned forum post information and the time it was executed (scraped_time)
        """
        forum_data = self.scraper.scrape_page(page_num)
        print(forum_data)
        scraped_time = str(dt.now())
        return forum_data, scraped_time

    def get_price_reports(self, data):
        price_reports = []
        for d in data:
            reps = PostCleaner.clean_post(d.post_body)
            price_reports += reps
            print(reps)
        return price_reports

    def get_posts_and_reports(self):
        #TODO: roll get_price_reports and get_clean_forum_posts into a single function
        #return clean_forum_posts, price_reports
        pass
