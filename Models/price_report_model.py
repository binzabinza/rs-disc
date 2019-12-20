class PriceReportModel:
    """
    A model that contains info about a price report.

    ...

    Attributes
    ----------
    item_id : int
        a unique id for the item reported
    transaction_type : str
        a str defining the transaction type of the price report (one of: "nib", "nis", "inb", "ins")
    price : int
        the price that was reported
    time : str
        the timestamp of the post which contains this price report
    thread_id : int
    page_id : int
        page number in the thread of the post which contains this price report
    post_id : int
        the position of the post on the page
    """
    
    def __init__(self, item_id, transaction_type, price, time, thread_id, page_id, post_id):
        self.item_id = item_id
        self.transaction_type = transaction_type
        self.price = price
        self.time = time
        self.thread_id = thread_id
        self.page_id = page_id
        self.post_id = post_id