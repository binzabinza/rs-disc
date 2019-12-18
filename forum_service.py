from rs_scraper import RSScraper
import sqlite3

class ForumService:
    """
        Handles database I/O, calling the scraper, cleaning data, etc
    """
    def __init__(self):
        self.db_connection = sqlite3.connect('rs-forum.db')

    ##################
    # Database Methods
    ##################
    def __fetch_active_threads__(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT url FROM threads WHERE active=1')
        threads = cursor.fetchall()
        cursor.close()
        return threads

    def track_new_thread(self, url):
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO threads (url, active) VALUES (?, ?)', (url, 1))
        self.db_connection.commit()
        cursor.close()

    ##################
    # Scraping Methods
    ##################
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