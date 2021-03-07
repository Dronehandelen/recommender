import logging
from sanic import Sanic
from sanic.response import json
import sentry_sdk
from sentry_sdk.integrations.sanic import SanicIntegration

import app.config.app as app_config
from app.cron import Crons
from app.orderProductRater import OrderProductRater
from app.productEventBySessionRater import ProductEventBySessionRater
from app.productEventRater import ProductEventRater
from sanic.exceptions import abort

from app.services.logging import setup_logging

if app_config.is_prod:
    sentry_sdk.init(
       dsn=app_config.sentry_url,
       integrations=[SanicIntegration()]
    )

setup_logging()
order_product_rater = OrderProductRater()
product_events_rater = ProductEventRater()
product_events_by_session_rater = ProductEventBySessionRater()


def update_corr_tables():
    logging.info("Cron triggering update of corr tables")
    order_product_rater.update_recommender()
    product_events_rater.update_recommender()
    product_events_by_session_rater.update_recommender()


crons = Crons()

crons.every().hour.do(update_corr_tables)

crons.run()


def predict(product_ids, count=10):
    rated_list = [
        order_product_rater.rate(product_ids),
        # product_events_rater.rate(product_ids),
        product_events_by_session_rater.rate(product_ids),
    ]

    result_unsorted = None
    x = 1
    for rate in rated_list:
        x = x + 1
        if rate is None:
            continue

        if result_unsorted is None:
            result_unsorted = rate
        else:
            result_unsorted = result_unsorted.join(rate, on="productId")

    if result_unsorted is None:
        return []

    result_unsorted = result_unsorted.fillna(0)
    result_unsorted["result"] = result_unsorted.sum(axis=1)
    result = result_unsorted["result"].drop(product_ids, errors="ignore").sort_values(ascending=False).dropna()
    return result.reset_index()["productId"].head(count).to_list()


app = Sanic("DH recommender")


@app.route("/recommend/product-ids", methods=["POST"])
async def recommend_for_products(request):
    product_ids = request.json.get("productIds")
    if product_ids is None or not isinstance(product_ids, list) or len(product_ids) == 0:
        abort(422)

    return json({"productIds": predict(product_ids)})


app.run(port=80, host="0.0.0.0")
