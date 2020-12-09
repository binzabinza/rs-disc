from rs_scraper import RSScraper
from post_cleaner import PostCleaner
from datetime import datetime as dt
from typing import List, Tuple
from Models.forum_post_model import ForumPostModel
from Models.price_report_model import PriceReportModel

from concurrent.futures import ThreadPoolExecutor, as_completed, wait

from time import time

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

        scraped_time = str(dt.now())

        posts = []
        with ThreadPoolExecutor(max_workers=24) as executor:
            processes = {
                executor.submit(self.scraper.scrape_page, page_number) : page_number
                for page_number in range(page_start, page_end)
            }

            for process in as_completed(processes):
                page_number = processes[process]
                try:
                    raw_posts = process.result()
                except Exception as exc:
                    print(f'exception occurred while trying to get posts on page {page_number}: {exc}')
                else:
                    posts_on_page = PostCleaner.prepare_forum_data(raw_posts, thread_id, scraped_time)
                    print(f'got {len(posts_on_page)} posts from page {page_number}')
                    posts += posts_on_page

        price_reports = []
        for post in posts:
            price_reports += PostCleaner.extract_price_reports(post = post)

        return (posts, price_reports)

    def __get_raw_forum_post__(self, url, page_num):
        """
            Takes a url and a page_num
            returns a list of uncleaned forum post information and the time it was executed (scraped_time)
        """
        forum_data = self.scraper.scrape_page(page_num)
        print(forum_data)
        scraped_time = str(dt.now())
        return forum_data, scraped_time