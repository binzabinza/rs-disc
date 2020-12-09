from sqlalchemy import exists
from typing import List
import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import db_manager as db
from models import *
from item_ids.api_manager import *
from utilities import log_manager

log = log_manager.get_logger('RS3ItemIds.main')


def save_items_block(items: List[Item]):
    with db.session_scope() as session:
        # session.query(Item).filter(Item.id in items).delete()
        [session.query(Item).filter(Item.id == i.id).delete() for i in items]
        session.add_all(items)


def save_item_page_block(item_page: ItemPage, item_count: int) -> int:
    """
    Saves or updates an item page.

    :returns The ID of the item page if the save operation was successful.
    """
    with db.session_scope() as session:
        existing_entry: ItemPage = ItemPage.fetch_where(
            session=session,
            item_category_id=item_page.item_category_id,
            alpha=item_page.alpha,
            page_num=item_page.page_num
        )
        if not len(existing_entry):
            item_page.save_in(session)
        else:
            existing_entry = existing_entry[0]
            if not item_page.succeeded and item_count < len(existing_entry.items):
                log.info(f'Received less items for page (category_id={item_page.category_id}, '
                         f'alpha={item_page.alpha}, page_num={item_page.page_num}) than what was already stored. '
                         f'Not saving.')
            else:
                log.info(f'Replacing entry for ItemPage (item_category_id={item_page.item_category_id}, '
                         f'alpha={item_page.alpha}, page_num={item_page.page_num})')

                existing_entry.item_category_id = item_page.item_category_id
                existing_entry.alpha = item_page.alpha
                existing_entry.page_num = item_page.page_num
                existing_entry.last_updated = item_page.last_updated
                existing_entry.succeeded = item_page.succeeded

    with db.session_scope() as session:
        item_page: ItemPage = ItemPage.fetch_where(
            session=session,
            item_category_id=item_page.item_category_id,
            alpha=item_page.alpha,
            page_num=item_page.page_num
        )[0]

        return item_page.id


def update_category_block(category: ItemCategory):
    with db.session_scope() as session:
        existing_entry = ItemCategory.fetch_by_primary(category.id, session=session)
        existing_entry.expected_item_count = category.expected_item_count
        existing_entry.item_count = category.item_count


def main():
    categories = ItemCategory.fetch_all()
    for category in categories:
        print(f'\n\n{category.id}, {category.name}\n\n')
        get_items_in_category(category, save_items_block, save_item_page_block, update_category_block)


if __name__ == '__main__':
    main()
