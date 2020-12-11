from typing import List, Optional, Tuple
import re
from datetime import datetime

from models import *
from Items.items import all_items
from utilities import log_manager

log = log_manager.get_logger('RS3RareItemPrices.post_cleaner')


def datetime_from_string(time_string) -> datetime:
    try:
        timestamp = datetime.strptime(time_string, '%d-%b-%Y %H:%M:%S')
    except ValueError:
        print(time_string)
    else:
        return timestamp


def extract_timestamp(ts_string) -> Tuple[datetime, Optional[datetime]]:
    """
    will return two timestamps as strings. The first is the timestamp of the original post. The second,
    if it exists, will be the timestamp of the edit otherwise NoneType
    """
    cleaned_original_ts = ts_string.replace('\n', '').strip(' \t\r\n')
    # executes if a post has been edited
    if len(cleaned_original_ts) > 20:
        edit_time = cleaned_original_ts[39:59].strip(' \t\r\n')
        original_time = cleaned_original_ts[:20]
        return datetime_from_string(original_time), datetime_from_string(edit_time)
    else:
        return datetime_from_string(cleaned_original_ts), None


def extract_price_reports(post: ForumPost) -> List[PriceReport]:
    """
    takes a post and returns a list of properly formatted price reports found in the post's body
    """
    post_body = post.post_body.lower()

    report_pattern = r'(nib|nis|inb|ins) (.*) (\d+)([a-z]*)'
    raw_reports = re.findall(report_pattern, post_body)

    reports = []
    for raw_report in raw_reports:
        item_id = __find_item_id(raw_report[1])
        if not item_id: continue

        reports.append(
            PriceReport(
                item_id=item_id,
                transaction_type=raw_report[0],
                price=raw_report[2],
                timestamp=post.timestamp,
                thread_id=post.thread_id,
                page_num=post.page_num,
                post_num=post.post_num
            )
        )

    return reports


def __find_item_id(raw_str: str) -> Optional[int]:
    """
    takes a str that might contain an item name and does a fuzzy search for
    a substring matching any of the items listed in Items.py

    Parameters
    ----------
    raw_str : str
        The raw string that may contain an items name.

    Returns
    -------
    str
        Either the item id or None if no match was found.
    """

    for key in all_items.keys():
        if key in raw_str:
            name = all_items[key]
            match = Item.fetch_where(name=name)
            return match[0] if match else None

    # no match found, return empty string
    log.warning(f'No item id found for raw string: {raw_str}')
    return None


def prepare_forum_data(raw_posts, thread_id, scraped_time: datetime) -> List[ForumPost]:
    """
    takes raw forum posts (list of tuples) and cleans it.

    Returns
    -------
    List[ForumPost]
        A list of ForumPost objects.
    """

    posts = []
    for p in raw_posts:
        timestamp, edit_timestamp = extract_timestamp(p[0])
        posts.append(ForumPost(
            thread_id=thread_id,
            page_num=p[4],
            post_num=p[3],
            username=p[1],
            post_body=p[2],
            timestamp=timestamp,
            edit_timestamp=edit_timestamp,
            scraped_timestamp=scraped_time
        ))

    return posts
