import sqlite3

#NOTE: it may both readability and memory if data is passed to database methods via a dictionary.
class DBManager:

    def __init__(self, db_name='rs-forum.db', display=False):
        self.db_connection = sqlite3.connect(db_name)

        self.display = display #if display is true, db_manager will write information to the terminal

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

    def fetch_forum_posts(self, thread_id):
        #we can definitely make this bad boy more powerful
        cursor = self.db_connection.cursor()
        sql_command = "SELECT * FROM forum_posts WHERE thread_id = ?"
        cursor.execute(sql_command, (thread_id,))
        forum_posts = cursor.fetchall()
        cursor.close()
        return forum_posts

    #########################
    # insert methods (INSERT)
    #########################
    def track_new_thread(self, url):
        """
            starts tracking a new thread by adding some info to the threads table. When a new thread is tracked, it automatically
            sets the values (last_page_num, last_post_num) to (1,1).
            Returns the thread_id
        """
        cursor = self.db_connection.cursor()
        sql_command = "INSERT INTO threads (url, active, last_page_num, last_post_num) VALUES (?, ?, ?, ?)"
        try:
            cursor.execute(sql_command, (url, 1, 1, 1))
        except sqlite3.IntegrityError:
            if display : print("already tracked")
        else:
            self.db_connection.commit()
        finally:
            sql_command = "SELECT thread_id FROM threads WHERE url=?"
            cursor.execute(sql_command, (url,))
            thread_id = cursor.fetchone()[0]
            cursor.close()
            return thread_id

    def insert_forum_post(self, forum_posts, force=False):
        """
        if force is passed as True, then this function will overwrite any database conflicts
        if display is passed as True, then this function will output information to the terminal
        forum_posts should either be a single ForumPostModel object, or a list of ForumPostModel objects
        returns a tuple containing the number of successful insertions and the number of conflicts
        """
        cursor = self.db_connection.cursor()
        sql_command = "INSERT INTO forum_posts (thread_id, timestamp, username, post_body, post_num, page_num, scraped_timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)"
        #one quick line handling an input of a single data point
        if type(forum_posts) != list : forum_posts = [forum_posts]

        conflict_count = 0

        for post in forum_posts:
            try:
                cursor.execute(sql_command, (post.thread_id, post.timestamp, post.username, post.post_body, post.post_num, post.page_num, post.scraped_timestamp))
            except sqlite3.IntegrityError:
                conflict_count += 1
                if (force):
                    cursor.execute('UPDATE forum_posts SET timestamp=?, username=?, post_body=?, scraped_timestamp=? WHERE thread_id=? AND post_num=? AND page_num=?', (post.timestamp, post.username, post.post_body, post.scraped_timestamp, post.thread_id, post.post_num, post.page_num))
                    if self.display : print("overwrite post {}.{}.{}".format(*post.identifier()))
                else:
                    if self.display : print("already scraped post {}.{}.{}".format(*post.identifier()))
        
        self.db_connection.commit()
        cursor.close()

        successful = len(forum_posts) - conflict_count
        return successful, conflict_count

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