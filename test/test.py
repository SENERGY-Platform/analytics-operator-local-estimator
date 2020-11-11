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
from datetime import datetime, timezone, timedelta
import unittest
import numpy as np
from dateutil.relativedelta import *
import main


class TestMainMethods(unittest.TestCase):

    def test_predict(self):
        n_samples = 0
        max_samples = 744
        data = np.random.randint(6, size=max_samples)
        target_value = np.sum(data)
        today = datetime.utcnow().date()
        dt = datetime(today.year, 1, 1)
        target = datetime(today.year, 2, 1)
        target_timestamp = target.replace(tzinfo=timezone.utc).timestamp()
        val = 0
        while n_samples < max_samples:
            val = val + data[n_samples]
            timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
            x, y = np.array([[timestamp, 1]]), np.array([val])
            print(x, y)
            main.train(val, timestamp)
            pred = main.predict(target_timestamp)
            print(pred)
            print(pred / target_value)
            print("*******************")
            dt = dt + timedelta(hours=1)
            n_samples += 1

    def test_date(self):
        today = datetime(2013, 12, 31)
        eoy = datetime(today.year, 12, 31)
        eom = datetime(today.year, today.month, 1)+relativedelta(months=1)
        eod = datetime(today.year, today.month, today.day)+timedelta(days=1)
        print(eoy)
        print(eom)
        print(eod)
