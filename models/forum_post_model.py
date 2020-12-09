from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models import Model


class ForumPost(Model):
    """
    A model that contains info about a forum post.
    """

    __tablename__ = 'forum_posts'

    thread_id = Column(Integer, ForeignKey('forum_threads.id'), primary_key=True)
    """Unique ID for the thread this post was found in."""

    thread = relationship('ForumThread', back_populates='posts')

    page_num = Column(Integer, primary_key=True)
    """Page number in the thread that this post was found on."""

    post_num = Column(Integer, primary_key=True)
    """The index on the page of this post."""

    username = Column(String)
    """The username of the poster."""

    post_body = Column(String)
    """The body text of this post."""

    timestamp = Column(DateTime)
    """The time this post was published."""

    edit_timestamp = Column(DateTime, nullable=True)
    """The time this post was edited (can be None)."""

    scraped_timestamp = Column(DateTime)
    """The time this post was scraped."""

    price_reports = relationship('PriceReport', back_populates='forum_post')
    """List of PriceReport objects found in this post."""

    @classmethod
    def from_array(cls, data):
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


if __name__ == '__main__':
    pass
