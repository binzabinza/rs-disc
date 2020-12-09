from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint
from datetime import datetime
from models import Model


class PriceReport(Model):
    """
    A model that contains info about a price report.
    """

    __tablename__ = 'price_reports'

    id = Column(Integer, primary_key=True)
    """Unique id for the item report."""

    item_id = Column(Integer)
    """Unique ID of the item that this report is for."""

    transaction_type = Column(String)
    """The transaction type of the price report (one of: "nib", "nis", "inb", "ins")"""

    price = Column(Integer)
    """The price that was reported"""

    timestamp = Column(DateTime)
    """Timestamp of the post which contains this price report"""

    thread_id = Column(Integer)
    """ID of the thread this report was found in."""

    page_num = Column(Integer)
    """Page number in the thread that this report was found on."""

    post_num = Column(Integer)
    """Post number on the page that this report was found in."""

    forum_post = relationship('ForumPost', back_populates='price_reports')
    """The ForumPost whose body contained this price report."""

    __table_args__ = (
        ForeignKeyConstraint(
            ('thread_id', 'page_num', 'post_num'),
            ('forum_posts.thread_id', 'forum_posts.page_num', 'forum_posts.post_num')
        ),
    )
    
    @classmethod
    def from_array(cls, data):
        obj = cls(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        return obj
    
    def __str__(self):
        meta  = "Post #{}.{}.{}".format(self.thread_id, self.page_num, self.post_num)
        report  = "{} {}  - {}".format(self.transaction_type, self.price, self.time)
        return report + "\n" + meta


if __name__ == '__main__':
    pass
