from app.rater import Rater


class OrderProductRater(Rater):
    def __init__(self):
        Rater.__init__(self, "order_product", "order_products")

    def get_corr_table(self, csv_data):
        csv_data["value"] = 1
        return csv_data.pivot_table(index="orderId", columns="productId", values="value", fill_value=0).corr()