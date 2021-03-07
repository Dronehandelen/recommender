from app.rater import Rater


class ProductEventRater(Rater):
    def __init__(self):
        Rater.__init__(self, "product_event", "product_events")

    def get_corr_table(self, csv_data):
        csv_data["value"] = 1
        return csv_data.pivot_table(index="trackingUserId", columns="productId", values="value", fill_value=0).corr()
