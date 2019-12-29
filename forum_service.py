from rs_scraper import RSScraper
from post_cleaner import PostCleaner
from datetime import datetime as dt

class ForumService:
    """
        Handles the scraping calls and cleaning data
    """

    def get_forum_posts(self, url, thread_id, page_start, page_end=''):
        """
            Takes a url, thread_id, page_start, and optionally, a page_end
            it will return a list of ForumPostModel objects containing properly formatted forum post information
            for the specified page range. defaults to last page if a specific page is not specified
        """
        if (page_end == '') : page_end = RSScraper(url).get_max_page() + 1 #NOTE: is this bad practice??
        result = []
        for page_index in range(page_start, page_end):
            result += (self.get_forum_post(url, thread_id, page_index))
        return result

    def get_forum_post(self, url, thread_id, page_num):
        """
            Takes a url, thread_id, and a page_num
            it will return a list of ForumPostModel objects containing properly formatted forum post information
            for a single page
        """
        forum_data, scraped_time = self.__get_raw_forum_post__(url, page_num)
        clean_forum_data = PostCleaner.prepare_forum_data(forum_data, thread_id, scraped_time)
        return clean_forum_data
    
    def __get_raw_forum_post__(self, url, page_num):
        """
            Takes a url and a page_num
            returns a list of uncleaned forum post information and the time it was executed (scraped_time)
        """
        scraper = RSScraper(url)
        forum_data = scraper.scrape_page(page_num)
        scraped_time = str(dt.now())
        return forum_data, scraped_time

    def get_price_reports(self):
        #TODO: implement the creating/cleaning of price reports
        pass

    def get_posts_and_reports(self):
        #TODO: roll get_price_reports and get_clean_forum_posts into a single function
        #return clean_forum_posts, price_reports
        pass