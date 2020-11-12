#  Copyright 2020 InfAI (CC SES)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import typing
from datetime import datetime, timedelta, timezone

from senergy_local_analytics import App, Input, Output
from skmultiflow.trees import HoeffdingTreeRegressor
import numpy as np
from dateutil.relativedelta import *

ht_reg = HoeffdingTreeRegressor()


def train(value, current_timestamp):
    x, y = np.array([[current_timestamp, 1]]), np.array([value])
    ht_reg.partial_fit(x, y)


def predict(target_timestamp):
    pred = ht_reg.predict(np.array([[target_timestamp, 1]]))
    return pred[0]


def process(inputs: typing.List[Input]):
    today = datetime.utcnow().date()
    eoy = datetime(today.year, 12, 31)
    eom = datetime(today.year, today.month, 1) + relativedelta(months=1)
    eod = datetime(today.year, today.month, today.day) + timedelta(days=1)

    value = 0
    dt = datetime.now()
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    ts = ""
    message_id = ""
    for inp in inputs:
        if inp.name == "value" and inp.current_value is not None:
            value = inp.current_value
        if inp.name == "timestamp" and inp.current_value is not None:
            ts = inp.current_value
        if inp.name == "message_id" and inp.current_value is not None:
            message_id = inp.current_value
    train(value, timestamp)
    pred_day = predict(eod.replace(tzinfo=timezone.utc).timestamp())
    pred_month = predict(eom.replace(tzinfo=timezone.utc).timestamp())
    pred_year = predict(eoy.replace(tzinfo=timezone.utc).timestamp())
    return Output(True, {"pred_day": pred_day, "pred_day_timestamp": str(eod),
                         "pred_month": pred_month, "pred_month_timestamp": str(eom),
                         "pred_year": pred_year, "pred_year_timestamp": str(eoy),
                         "message_id": message_id,
                         "timestamp": ts
                         })


if __name__ == '__main__':
    app = App()

    input1 = Input("value")
    input2 = Input("timestamp")
    input3 = Input("message_id")

    app.config([input1, input2, input3])
    print("start operator", flush=True)
    app.process_message(process)
    app.main()
