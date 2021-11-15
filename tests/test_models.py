import json
import time
import unittest
from datetime import datetime
from pathlib import Path

from pebbleMap.model import Plano


class TestPlanoModel(unittest.TestCase):
    DATA_PATH = Path("tests/data")
    start = datetime.now()
    end = datetime.now()
    curse = 123

    @classmethod
    def setUpClass(cls):
        Plano.data = cls.mocked_data

    @staticmethod
    def mocked_data(start: datetime, end: datetime, course_id: int):
        path = TestPlanoModel.DATA_PATH / "plano.raw.json"
        with open(path, "r") as file:
            return json.load(file)

    def test_data_mock(self):
        self.assertEqual(
            TestPlanoModel.mocked_data(self.start, self.end, self.curse),
            Plano.data(self.start, self.end, self.curse)
        )

    def test_occupancy(self):
        path = TestPlanoModel.DATA_PATH / "plano.occupancy.json"
        with open(path, "r") as file:
            expectation = json.load(file)

        result = [s.participants for s in Plano.occupancy(self.start, self.end, self.curse)]

        self.assertEqual(expectation, result)

    @unittest.skip("Only performance testing")
    def test_occupancy_speed(self):
        rounds = 30
        start = time.time()
        for i in range(rounds):
            Plano.occupancy(self.start, self.end, self.curse)
        delta = time.time() - start
        print(f'{delta/rounds*1000:0.2f}ms', "per occupancy call")




