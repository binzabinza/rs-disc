from __future__ import annotations
from typing import Any

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
    edit_timestamp : str
        cleaned edit timestamp, can be None
    scraped_timestamp : str
        the raw timestamp as it was posted
    """

    def __init__(
        self,
        thread_id: int,
        page_num: int,
        post_num: int,
        username: str,
        post_body: str,
        timestamp: str,
        edit_timestamp: str,
        scraped_timestamp: str
    ):
        self.thread_id = thread_id
        self.page_num = page_num
        self.post_num = post_num
        self.username = username
        self.post_body = post_body
        self.timestamp = timestamp
        self.edit_timestamp = edit_timestamp
        self.scraped_timestamp = scraped_timestamp
    
    @classmethod
    def from_array(cls, data: Any) -> ForumPostModel:
        obj = cls(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
        return obj
    
    #NOTE: this works, but i dont know if it is good practice
    # def __init__(self, *args, **kwargs):
    #     if len(args) == 8:
    #         self.from_array(list(args))
    #     elif len(args) == 1:
    #         self.from_array(args[0])

    def identifier(self):
        """
            returns the identifying numbers for the post
        """
        return (self.thread_id, self.page_num, self.post_num)

    def __str__(self):
        line  = "\n------------------------------------------------------------------\n"
        meta  = "Post #{}.{}.{} - {}\n".format(self.thread_id, self.page_num, self.post_num, self.scraped_timestamp)
        post  = "{}\n\t{}\nPosted: {}, Edited: {}".format(self.username, self.post_body, self.timestamp, self.edit_timestamp)
        return line + meta + post + line 
