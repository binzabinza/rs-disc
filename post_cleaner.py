from Models.forum_post_model import ForumPostModel
class PostCleaner:

    @staticmethod
    def clean_timestamp(ts_string):
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
    def clean_post(pb_string):
        """
        takes a raw post body and returns a list of properly formatted price reports
        """
        pass

    @classmethod
    def prepare_forum_data(cls, data, thread_id, scraped_time):
        """
        takes raw forum data (list of tuples) and cleans it.
        
        Returns
        --------
        list
            a list of `ForumPostModel` objects.
        """
        for i, post in enumerate(data):
            time, edit_time = cls.clean_timestamp(post[0])
            data[i] = ForumPostModel(thread_id, post[4], post[3], post[1], post[2], time, edit_time, scraped_time)
        return data