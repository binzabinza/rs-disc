from rs_scraper import RSScraper
import post_cleaner
from datetime import datetime as dt
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

from models import *
from utilities import log_manager

log = log_manager.get_logger('RS3RareItemPrices.forum_service')


class ForumService:
    """Handles the scraping calls and cleaning data"""

    def __init__(self, url):
        self.url = url
        self.scraper = RSScraper(url)

    def get_forum_posts_and_reports(
            self,
            thread_id: str,
            page_start: int,
            page_end: int = 0
    ) -> Tuple[List[ForumPost], List[PriceReport]]:
        """
            Takes a url, thread_id, page_start, and optionally, a page_end
            it will return a list of ForumPost objects containing properly formatted forum post information
            for the specified page range. defaults to last page if a specific page is not specified
        """
        if not page_end: page_end = self.scraper.get_max_page() + 1

        scraped_time = dt.now()

        posts = []
        with ThreadPoolExecutor(max_workers=24) as executor:
            processes = {
                executor.submit(self.scraper.scrape_page, page_number): page_number
                for page_number in range(page_start, page_end)
            }

            for process in as_completed(processes):
                page_number = processes[process]
                try:
                    raw_posts = process.result()
                except Exception as exc:
                    log.warning(f'Exception occurred while trying to get posts on page {page_number}', exc_info=exc)
                else:
                    posts_on_page = post_cleaner.prepare_forum_data(raw_posts, thread_id, scraped_time)
                    log.debug(f'Got {len(posts_on_page)} posts from page {page_number}')
                    posts += posts_on_page

        price_reports = []
        for post in posts:
            price_reports += post_cleaner.extract_price_reports(post=post)

        return posts, price_reports

    def __get_raw_forum_post__(self, page_num: int):
        """
            Takes a url and a page_num
            returns a list of uncleaned forum post information and the time it was executed (scraped_time)
        """
        forum_data = self.scraper.scrape_page(page_num)
        print(forum_data)
        scraped_time = str(dt.now())
        return forum_data, scraped_time
