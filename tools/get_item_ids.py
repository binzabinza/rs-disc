import sqlite3, requests, sys, time

CATEGORY_LIMIT = 41
#12 items per page


class Bullshit:
    def __init__(self):
        self.category_base_url = "http://services.runescape.com/m=itemdb_rs/api/catalogue/category.json?category={}"
        self.items_base_url    = "http://services.runescape.com/m=itemdb_rs/api/catalogue/items.json?category={}&alpha={}&page={}"
        self.db_connection     = sqlite3.connect("rs-forum.db")

    def get_category_list(self, num):
        """
        Takes a category number, returns the number of items by letter
        """
        res = requests.get(self.category_base_url.format(num), headers={"Content-Type" : "application/json"})
        data = res.json()
        stripped_data = []
        for letx in data["alpha"]:
            letter = letx["letter"]
            quant  = letx["items"]
            if (quant != 0):
                stripped_data.append((letter, quant))
        self.data = stripped_data
        return stripped_data


    def generate_data(self):
        id_list = []
        for cat_num in range(CATEGORY_LIMIT):
            category_data = self.get_category_list(cat_num)
            for dat in category_data:
                alpha = dat[0]
                quant = dat[1]
                #handle urlencoding bullshit
                if (alpha == '#'): alpha = '%23'
                #calculate page_num range
                page_num_limit = quant//12 + 1
                for page_num in range(1, page_num_limit+1):
                    res = requests.get(self.items_base_url.format(cat_num, alpha, page_num), headers={"Content-Type" : "application/json"})
                    try:
                        jdata = res.json()
                    except:
                        #NOTE
                        #this is happening because of API rate limits
                        print(self.items_base_url.format(cat_num, alpha, page_num))
                        sys.exit()
                    item_list = jdata["items"]
                    for item in item_list:
                        id_list.append((item["id"], item["name"]))
        return id_list

    def insert_data(self, data):
        """
        Takes a list of tuples (preferably returned by self.generate_data) and inserts the id-value pairs into the items table
        """
        cursor = self.db_connection.cursor()
        sql_command = "INSERT INTO items (item_id, full_name) VALUES (?, ?)"
        cursor.executemany(sql_command, data)
        self.db_connection.commit()
        cursor.close()

b = Bullshit()
b.get_category_list
b.generate_data()