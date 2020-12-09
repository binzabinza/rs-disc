from models import *
import db_manager as db

from item_ids.rs3_api_constants import item_categories


def populate_item_categories():
    """Inserts categories generated from the categories dictionary in rs3_api_constants.py"""
    categories = [ItemCategory(id=category_id, name=name) for category_id, name in item_categories.items()]
    with db.session_scope() as session:
        session.add_all(categories)


def main():
    print('Generating Database')
    Model.metadata.create_all(db.engine)
    populate_item_categories()


if __name__ == '__main__':
    main()
