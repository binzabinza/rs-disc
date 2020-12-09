from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models import Model


class Item(Model):
    """
    Model of a RuneScape item.
    """

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=False)
    item_category_id = Column(Integer, ForeignKey('item_categories.id'), nullable=False)
    item_category = relationship('ItemCategory', back_populates='items')
    item_page_id = Column(Integer, ForeignKey('item_pages.id'), nullable=False)
    item_page = relationship('ItemPage', back_populates='items')
    name = Column(String, nullable=False)
    description = Column(String)
    type = Column(String)
    members_only = Column(Boolean)
