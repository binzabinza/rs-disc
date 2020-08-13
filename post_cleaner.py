from typing import List
import re

from Models.forum_post_model import ForumPostModel
from Models.price_report_model import PriceReportModel
from Items.Items import all_items

class PostCleaner:

    @staticmethod
    def extract_timestamp(ts_string):
        """
        will return two timestamps as strings. The first is the timestamp of the original post. The second,
        if it exists, will be the timestamp of the edit otherwise NoneType
        """
        cleaned_original_ts = ts_string.replace('\n', '').strip()
        #executes if a post has been edited
        if len(cleaned_original_ts) > 20:
            cleaned_edit_ts = cleaned_original_ts[39:59]
            return cleaned_original_ts[:20], cleaned_edit_ts
        else:
            return cleaned_original_ts, None

    @staticmethod
    def extract_price_reports(post: ForumPostModel) -> List[PriceReportModel]:
        """
        takes a post and returns a list of properly formatted price reports found in the post's body
        """
        post_body = post.post_body.lower()

        report_pattern = r'(nib|nis|inb|ins) (.*) (\d+)([a-z]*)'
        raw_reports = re.findall(report_pattern, post_body)

        reports = []
        for raw_report in raw_reports:
            item_id = PostCleaner.__find_item_id(raw_report[1])
            if item_id == '': continue

            reports.append(
                PriceReportModel(
                    item_id,
                    raw_report[0],
                    raw_report[2],
                    post.timestamp,
                    post.thread_id,
                    post.page_num,
                    post.post_num
                )
            )

        return reports

    @staticmethod
    def __find_item_id(raw_str: str) -> str:
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
            Either the item id or empty string if no match was found.
        """

        for key in all_items.keys():
            if key in raw_str:
                return all_items[key]
        
        # no match found, return empty string
        print(f'ERROR: No item id found for raw string: {raw_str}')
        return ''


    @classmethod
    def prepare_forum_data(cls, raw_posts, thread_id, scraped_time):
        """
        takes raw forum posts (list of tuples) and cleans it.
        
        Returns
        -------
        List[ForumPostModel]
            A list of `ForumPostModel` objects.
        """

        posts = []
        for p in raw_posts:
            timestamp, edit_timestamp = cls.extract_timestamp(p[0])
            posts.append(ForumPostModel(
                thread_id,
                p[4], p[3], p[1], p[2],
                timestamp,
                edit_timestamp,
                scraped_time
            ))

#        posts = [
#            ForumPostModel(
#                thread_id,
#                p[4], p[3], p[1], p[2],
#                cls.extract_timestamp(p[0]),
#                scraped_time
#            )
#            for p in raw_posts
#        ]

        return posts
