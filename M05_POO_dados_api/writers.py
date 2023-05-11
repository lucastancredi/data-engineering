from abc import ABC, abstractmethod
import datetime
import json
import logging
import os
import time
import ratelimit
from typing import Union, List
import requests
from schedule import repeat, every, run_pending
from backoff import expo, on_exception

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
      

class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported"
        super().__init__(self.message)

class DataWriter:

    def __init__(self, coin: str, api: str) -> None:
        self.api = api
        self.coin = coin
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        print(os.path.dirname(self.filename))
        with open(self.filename, "a") as f:
            f.write(row)
        
    def write(self, data: Union[List, dict]):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance (data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedForIngestionException(data)