class PostCleaner:

    def __init__(self):
        self.transaction_types = {'ins', 'inb', 'nic', 'nis'}

    def clean_timestamp(self, ts_string):
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

    def clean_post(self, pb_string):
        """
        takes a raw post body and returns a list of properly formatted price reports
        """
        pass

    def prepare_forum_data(self, data, thread_id, scraped_time):
        """
            this will properly order the data for database insertion
        """
        for i, post in enumerate(data):
            p = list(post)
            time, edit_time = self.clean_timestamp(p[0])
            data[i] = (thread_id, post[4], post[3], post[1], post[2], time, edit_time, scraped_time)
        return data