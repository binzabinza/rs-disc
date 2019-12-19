from rs_scraper import RSScraper

class ForumService:
"""
    Handles the scraper.
"""
    def __init__(self):
        pass

    ##################
    # Scraping Methods
    ##################
    def get_raw_posts(self, url, page_start, page_end=''):
        scraper = RSScraper(url)
        if (page_end == '') : page_end = scraper.max_page #defaults to last page if a specific page is not specified
        raw_posts = []
        for i in range(page_start, page_end):
            raw_posts += scraper.scrape_page(i)
        return raw_posts, scraper.current_page, scraper.current_post
        



    def get_all_price_posts(self, url):
        scraper = RSScraper(url)
        max_page = scraper.max_page
        return self.__get_price_posts__(url, 1, max_page)

    def get_price_posts(self, url, page_start, page_end):
        scraper = RSScraper(url)
        return self.__get_price_posts__(scraper, page_start, page_end)

    def __get_price_posts__(self, scraper, page_start, page_end):
        price_posts = []
        for i in range(page_start, page_end):
            price_posts += scraper.scrape_page(i)

        return price_posts

        # NOTE: this is where we clean/parse/save the post data