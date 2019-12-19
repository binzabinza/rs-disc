from datetime import datetime as dt
import sqlite3

class DBManager:

    def __init__(self, db_name='rs-forum.db'):
        self.db_connection = sqlite3.connect(db_name)

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
        """
        this method will untrack a thread
        """
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
        cursor.execute('INSERT INTO threads (url, active, last_page_num, last_post_num) VALUES (?, ?, ?, ?)', (url, 1, 1, 1))
        self.db_connection.commit()
        cursor.close()
        #should maybe add a boolean return 

    def insert_raw_posts(self, raw_data, thread_id):
        """
        raw_data should be a list of tuples in format (timestamp, username, post_body)
        will insert raw post data into the raw_posts table. We should aim to deprecate this
        """
        cursor = self.db_connection.cursor()
        for post in raw_data:
            cursor.execute('INSERT INTO raw_posts (thread_id, timestamp, username, post_body, post_num, page_num, scraped_timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)', (thread_id, post[0], post[1], post[2], post[3], post[4], str(dt.now())))
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
