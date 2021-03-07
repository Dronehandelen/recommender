from app.rater import Rater


class ProductEventBySessionRater(Rater):
    def __init__(self):
        Rater.__init__(self, "product_event_by_session", "product_events_by_session")

    def get_corr_table(self, csv_data):
        csv_data["value"] = 1
        return csv_data.pivot_table(index="trackingSessionId", columns="productId", values="value", fill_value=0).corr()
