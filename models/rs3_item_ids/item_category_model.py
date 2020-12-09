from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import Model


class ItemCategory(Model):
    """
    Model of a RuneScape item category.
    """

    __tablename__ = 'item_categories'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    expected_item_count = Column(Integer)
    item_count = Column(Integer)
    items = relationship('Item', back_populates='item_category')
    item_pages = relationship('ItemPage', back_populates='item_category')


