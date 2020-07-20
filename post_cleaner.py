from typing import List
from Models.forum_post_model import ForumPostModel
from Models.price_report_model import PriceReportModel
import re

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

        return [
            PriceReportModel(
                r[1], r[0], r[2], 
                post.timestamp, 
                post.thread_id,
                post.page_num,
                post.post_num
            )
            for r in raw_reports
        ]

    @classmethod
    def prepare_forum_data(cls, raw_posts, thread_id, scraped_time):
        """
        takes raw forum posts (list of tuples) and cleans it.
        
        Returns
        --------
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
