#script to create a sqlite3 database for the rs-disc project
#TODO: this would be a super convenient script to create a general version of

import sqlite3, argparse

parser = argparse.ArgumentParser(description="Automatically create an empty rs-disc database.")
parser.add_argument('-n', metavar="database name", type=str, required=False, default='rs-forum.db', help='sqlite3 database filename')
args = parser.parse_args()

#create table coommands
CREATE_ITEMS         = "CREATE TABLE items (item_id INTEGER PRIMARY KEY, full_name TEXT);"
CREATE_ITEM_LOOKUP   = "CREATE TABLE item_lookup (item_id INTEGER, short_name TEXT, FOREIGN KEY(item_id) REFERENCES items(item_id));"
CREATE_PRICE_REPORTS = "CREATE TABLE price_reports (item_id INTEGER, transaction_type TEXT, value REAL, time TEXT, thread_id INTEGER, page_id INTEGER, post_id INTEGER, FOREIGN KEY(item_id) REFERENCES items(item_id), FOREIGN KEY(thread_id) REFERENCES threads(thread_id));"
CREATE_THREADS       = "CREATE TABLE threads (thread_id INTEGER PRIMARY KEY, url TEXT, last_page_num INTEGER, last_post_num INTEGER, active INTEGER, CONSTRAINT url UNIQUE(url));"
CREATE_FORUM_POSTS   = "CREATE TABLE forum_posts (thread_id INTEGER, page_num INTEGER, post_num INTEGER, username TEXT, post_body TEXT, timestamp TEXT, edit_timestamp TEXT, scraped_timestamp TEXT, FOREIGN KEY(thread_id) REFERENCES threads(thread_id), CONSTRAINT u_posts UNIQUE(thread_id, page_num, post_num));"

commands = [CREATE_ITEMS, CREATE_ITEM_LOOKUP, CREATE_PRICE_REPORTS, CREATE_THREADS, CREATE_FORUM_POSTS]
#create database
conn = sqlite3.connect(args.n)
c = conn.cursor()

for command in commands:
    c.execute(command)
conn.commit()
conn.close()