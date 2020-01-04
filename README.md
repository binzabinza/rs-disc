# rs-disc

## Database Information
sqlite3           : 2.6.0
database filename : rs-forum.db

### Table Schemas
#### threads
| Column Name       |   Data Type  |
|:-----------------:|-------------:|
| thread_id         | integer      |
| url               | text         |
| last_page_num     | integer      |
| last_post_num     | text         |
| active            | integer      |

CREATE TABLE threads (thread_id INTEGER PRIMARY KEY, url TEXT, last_page_num INTEGER, last_post_num INTEGER, active INTEGER, CONSTRAINT url UNIQUE(url));

#### forum_posts
| Column Name       |   Data Type  |
|:-----------------:|-------------:|
| thread_id         | integer      |
| page_num          | integer      |
| post_num          | integer      |
| username          | text         |
| post_body         | text         |
| timestamp         | text         |
| edit_timestamp    | text         |
| scraped_timestamp | text         |

CREATE TABLE forum_posts (thread_id INTEGER, page_num INTEGER, post_num INTEGER, username TEXT, post_body TEXT, timestamp TEXT, edit_timestamp TEXT, scraped_timestamp TEXT, FOREIGN KEY(thread_id) REFERENCES threads(thread_id), CONSTRAINT u_posts UNIQUE(thread_id, page_num, post_num));

#### price_reports
| Column Name       |   Data Type  |
|:-----------------:|-------------:|
| item_id           | integer      |
| transaction_type  | text         |
| value             | real         |
| time              | text         |
| thread_id         | integer      |
| page_id           | integer      |
| post_id           | integer      |

CREATE TABLE price_reports (item_id INTEGER, transaction_type TEXT, value REAL, time TEXT, thread_id INTEGER, page_id INTEGER, post_id INTEGER, FOREIGN KEY(item_id) REFERENCES items(item_id), FOREIGN KEY(thread_id) REFERENCES threads(thread_id));

#### item_lookup
| Column Name       |   Data Type  |
|:-----------------:|-------------:|
| item_id           | integer      |
| short_name        | text         |

CREATE TABLE item_lookup (item_id INTEGER, short_name TEXT, FOREIGN KEY(item_id) REFERENCES items(item_id));

#### items
| Column Name       |   Data Type  |
|:-----------------:|-------------:|
| item_id           | integer      |
| full_name         | text         |

CREATE TABLE items (item_id INTEGER PRIMARY KEY, full_name TEXT);
