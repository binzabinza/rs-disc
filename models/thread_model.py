from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models import Model


class ForumThread(Model):
    """
    A model that represents a forum thread.
    """

    __tablename__ = "forum_threads"

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    last_page_num = Column(Integer, default=1)
    last_post_num = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)

    posts = relationship('ForumPost', back_populates='thread')
