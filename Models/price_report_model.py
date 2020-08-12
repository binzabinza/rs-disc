class PriceReportModel:
    """
    A model that contains info about a price report.

    ...

    Attributes
    ----------
    item_id : string 
        A unique id for the item reported (the name of the item).
    transaction_type : str
        A str defining the transaction type of the price report (one of: "nib", "nis", "inb", "ins")
    price : int
        The price that was reported
    time : str
        The timestamp of the post which contains this price report
    thread_id : int
    page_id : int
        Page number in the thread of the post which contains this price report
    post_id : int
        The position of the post on the page
    """
    
    def __init__(
        self,
        item_id: str,
        transaction_type: str,
        price: int,
        time: str,
        thread_id: int,
        page_id: int,
        post_id: int
    ):
        self.item_id = item_id
        self.transaction_type = transaction_type
        self.price = price
        self.time = time
        self.thread_id = thread_id
        self.page_id = page_id
        self.post_id = post_id

    @classmethod
    def from_array(cls, data):
        obj = cls(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        return obj
    
    def __str__(self):
        meta  = "Post #{}.{}.{}".format(self.thread_id, self.page_id, self.post_id)
        report  = "{} {}  - {}".format(self.transaction_type, self.price, self.time)
        return report + "\n" + meta
