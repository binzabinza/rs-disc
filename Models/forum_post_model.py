class ForumPostModel:
    """
    A model that contains info about a forum post.

    ...

    Attributes
    ----------
    thread_id : int
        unique id for the thread
    page_num : int
        page number in the thread of the post
    post_num : int
        post number on the page
    username : str
        the username of the poster
    post_body : str
        the body message of the post
    timestamp : str
        the cleaned timestamp
    scraped_timestamp : str
        the raw timestamp as it was posted
    """

    def __init__(self, thread_id, page_num, post_num, username, post_body, timestamp, scraped_timestamp)
        self.thread_id = thread_id
        self.page_num = page_num
        self.post_num = post_num
        self.username = username
        self.post_body = post_body
        self.timestamp = timestamp
        self.scraped_timestamp = scraped_timestamp