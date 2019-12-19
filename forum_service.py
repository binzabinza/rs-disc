from rs_scraper import RSScraper
from datetime import datetime as dt
import sqlite3

class ForumService:
    """
        Handles database I/O, calling the scraper, cleaning data, etc
    """
    def __init__(self):
        self.db_connection = sqlite3.connect('rs-forum.db')

    ##################
    # DATABASE METHODS
    ##################
    def fetch_active_threads(self):
        """
        this will give us the necessary info and all actively tracked threads
        """
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT url, last_page_num, last_post_num, thread_id FROM threads WHERE active=1')
        threads = cursor.fetchall()
        cursor.close()
        return threads

    def update_tracked_threads(self, thread_id, page_num, post_num):
        """
        This will update the threads table. I think I can make this method more abstract.
        """
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE threads SET last_page_num=?, last_post_num=? WHERE thread_id=?', (page_num, post_num, thread_id))
        self.db_connection.commit()
        cursor.close()

    def untrack_thread(self, thread_id):
        """this method will untrack a thread"""
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE threads SET active=0 WHERE thread_id = ?', (thread_id,))
        self.db_connection.commit()
        cursor.close()

    def track_new_thread(self, url):
        """
            starts tracking a new thread by adding some info to the threads table. When a new thread is tracked, it automatically
            sets the values (last_page_num, last_post_num) to (1,1). 
        """
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO threads (url, active, last_page_num, last_post_num) VALUES (?, ?)', (url, 1, 1, 1))
        self.db_connection.commit()
        cursor.close()
        #should maybe add a boolean return 

    def insert_raw_posts(self, raw_data):
        """
        will insert raw post data into the raw_posts table. We should aim to deprecate this
        """
        cursor = self.db_connection.cursor()
        for post in raw_data:
            cursor.execute('INSERT INTO raw_posts VALUES (?, ?, ?, ?)', (post[1], post[2], post[0], str(dt.now())))
        self.db_connection.commit()
        cursor.close()

    def insert_price_reports(self):
        """
        This will eventually replace the insert_raw_posts methods by storing cleaned information
        """
        pass

    def fetch_price_reports(self, item_name):
        """
        this will fetch all price reports for a specific item. NOTE: This may be to vague to be useful
        """
        cursor = self.db_connection.cursor()
        #cursor.execute('SELECT * FROM price_reports WHERE full_name = ?', (item_name,))
        cursor.execute('SELECT pr.* FROM price_reports pr, item_lookup il WHERE pr.item_id = il.item_id AND il.short_name = ?', (item_name,))
        price_reports = cursor.fetchall()
        return price_reports

    ##################
    # Scraping Methods
    ##################
    def scrape_active_threads(self):
        """
        this method will take all active threads, scrape them starting from last_page until max_page
        it will then insert raw post data into the raw_posts database <---replace this with cleaned data
        finally it updates the threads table with the last page/post information
        """
        active_threads = self.fetch_active_threads()
        for thread in active_threads:
            url, last_page, last_post, thread_id = thread
            scraper = RSScraper(url)
            for page_index in range(last_page, last_page+5):
                data = scraper.scrape_page(page_index)
                self.insert_raw_posts(data)
                self.update_tracked_threads(thread_id, scraper.current_page, scraper.current_post)



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