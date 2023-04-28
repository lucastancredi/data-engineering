import datetime
import time

from schedule import repeat, every, run_pending
from ingestors import *
from apis import *
from writers import *
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__=='__main__':

    day_summary_ingestor = DaySummaryIngestor(
        writer=DataWriter, 
        coins=["BTC", "LTC", "ETH"], 
        default_start_date=datetime.date(2022, 3, 6)
        )

    @repeat(every(2).seconds)
    def job():
        day_summary_ingestor.ingest()

    while True:
        run_pending()
        time.sleep(0.5)