from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models import Model


class ItemPage(Model):
    """
    Model of the response received for a page of items with given category_id and alpha.
    Used to track last update times and failed requests.
    """

    __tablename__ = 'item_pages'

    id = Column(Integer, primary_key=True)
    item_category_id = Column(Integer, ForeignKey('item_categories.id'), nullable=False)
    item_category = relationship('ItemCategory', back_populates='item_pages')
    alpha = Column(String)
    page_num = Column(Integer)
    last_updated = Column(DateTime)
    succeeded = Column(Boolean, default=False)
    items = relationship('Item', back_populates='item_page')
