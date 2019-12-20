from datetime import datetime as dt
import sqlite3

#NOTE: it may both readability and memory if data is passed to database methods via a dictionary.
class DBManager:

    def __init__(self, db_name='rs-forum.db'):
        self.db_connection = sqlite3.connect(db_name)

    ########################
    # fetch methods (SELECT)
    ########################
    def fetch_active_threads(self):
        """
        this will give us the necessary info and all actively tracked threads
        """
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT url, last_page_num, last_post_num, thread_id FROM threads WHERE active=1')
        threads = cursor.fetchall()
        cursor.close()
        return threads

    def fetch_price_reports(self, item_name):
        """
        this will fetch all price reports for a specific item. NOTE: This may be to vague to be useful
        """
        cursor = self.db_connection.cursor()
        #cursor.execute('SELECT * FROM price_reports WHERE full_name = ?', (item_name,))
        cursor.execute('SELECT pr.* FROM price_reports pr, item_lookup il WHERE pr.item_id = il.item_id AND il.short_name = ?', (item_name,))
        price_reports = cursor.fetchall()
        return price_reports

    #########################
    # insert methods (INSERT)
    #########################
    def track_new_thread(self, url):
        """
            starts tracking a new thread by adding some info to the threads table. When a new thread is tracked, it automatically
            sets the values (last_page_num, last_post_num) to (1,1).
            Returns True if inserted, False if it encounters a conflict
        """
        cursor = self.db_connection.cursor()
        try:
            cursor.execute('INSERT INTO threads (url, active, last_page_num, last_post_num) VALUES (?, ?, ?, ?)', (url, 1, 1, 1))
        except sqlite3.IntegrityError:
            print("already tracked") #NOTE: some better kind of return here?
            return False
        else:
            self.db_connection.commit()

        cursor.close()
        return True

    def insert_raw_post(self, raw_data, thread_id, force=False):
        """
        if force is passed as True, then raw_posts will overwrite any conflicts
        raw_data should be a list of tuples in format (timestamp, username, post_body)
        will insert raw post data into the raw_posts table. We should aim to deprecate this
        Returns True if inserted, False if it encounters a conflict
        """
        cursor = self.db_connection.cursor()
        sql_command = "INSERT INTO raw_posts (thread_id, timestamp, username, post_body, post_num, page_num, scraped_timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)"
        try:
            cursor.execute(sql_command, (thread_id, raw_data[0], raw_data[1], raw_data[2], raw_data[3], raw_data[4], str(dt.now())))
        except sqlite3.IntegrityError:
            if (force):
                cursor.execute('UPDATE raw_posts SET timestamp=?, username=?, post_body=?, scraped_timestamp=? WHERE thread_id=? AND post_num=? AND page_num=?', (post[0], post[1], post[2], str(dt.now()), thread_id, post[3], post[4]))
                print("overwrite post {}.{}.{}".format(thread_id, post[4], post[3]))
            else:
                print("already scraped post {}.{}.{}".format(thread_id, post[4], post[3]))
        finally:
            self.db_connection.commit()
        cursor.close()
        return True

    def insert_many_raw_posts(self, raw_data, thread_id, force=False):
        """
        if force is passed as True, then raw_posts will overwrite any conflicts
        raw_data should be a list of tuples in format (timestamp, username, post_body)
        will insert raw post data into the raw_posts table. We should aim to deprecate this
        Returns True if inserted, False if it encounters a conflict
        """
        cursor = self.db_connection.cursor()
        for post in raw_data:
            try:
                cursor.execute('INSERT INTO raw_posts (thread_id, timestamp, username, post_body, post_num, page_num, scraped_timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)', (thread_id, post[0], post[1], post[2], post[3], post[4], str(dt.now())))
            except sqlite3.IntegrityError:
                if (force):
                    cursor.execute('UPDATE raw_posts SET timestamp=?, username=?, post_body=?, scraped_timestamp=? WHERE thread_id=? AND post_num=? AND page_num=?', (post[0], post[1], post[2], str(dt.now()), thread_id, post[3], post[4]))
                    print("overwrite post {}.{}.{}".format(thread_id, post[4], post[3]))
                else:
                    print("already scraped post {}.{}.{}".format(thread_id, post[4], post[3]))
            finally:
                self.db_connection.commit()
        cursor.close()
        return True

    def insert_price_reports(self):
        """
        This will eventually replace the insert_raw_posts methods by storing cleaned information
        """
        pass

    ##############################
    # change current info (UPDATE)
    ##############################
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