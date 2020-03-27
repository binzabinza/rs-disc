import os
from db_manager import DBManager
from Models.forum_post_model import ForumPostModel


class DiscordManager:
    def __init__(self):
        self.databasemanager = DBManager(debugging=True)
    
    def execute(self, command, args):
        if (command == "$help"):
            return "Help Menu Incoming"
        elif (command == "$track"):
            thread_id = self.databasemanager.track_new_thread(args[0])
            return thread_id
        elif (command == "$untrack"):
            self.databasemanager.untrack_thread(args[0])
        elif (command == "$ffetch"):
            if (len(args) == 1):
                posts = self.databasemanager.fetch_forum_posts(args[0])
            elif (len(args) == 2):
                posts = self.databasemanager.fetch_forum_posts(args[0], args[1])
            msg = ""
            for p in posts:
                thread_id = p[0]
                page_num  = p[1]
                post_num  = p[2]
                url = self.databasemanager.generate_link(thread_id, page_num, post_num)
                msg +=  str(ForumPostModel.from_array(p)) + url
            return msg
        elif (command == "$pfetch"):
            return "Data cleaning algorithms still need to be implemented"
        
