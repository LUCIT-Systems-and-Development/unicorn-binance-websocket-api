from unicorn_binance_websocket_api import BinanceWebSocketApiManager
import asyncio
import logging
import os

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


class BinanceDataProcessor:
    def __init__(self):
        self.ubwa = BinanceWebSocketApiManager(exchange='binance.com',
                                               process_asyncio_queue=self.process_asyncio_queue_global,
                                               enable_stream_signal_buffer=True,
                                               process_stream_signals=self.processing_of_stream_signals,
                                               output_default="dict",
                                               high_performance=True)
        self.stream_id1 = None
        self.stream_id2 = None

    async def process_asyncio_queue_global(self):
        print(f"Start processing data of {self.stream_id1} ...")
        last_update_id = 0
        while True:
            data = await self.ubwa.get_stream_data_from_asyncio_queue(self.stream_id1)
            if data.get('data'):
                current_update_id = data.get('data').get('lastUpdateId')
                print(f"{last_update_id} - {current_update_id} - "
                      f"{('True' if current_update_id > last_update_id else 'False')}")
                last_update_id = current_update_id
            self.ubwa.asyncio_queue_task_done(self.stream_id1)

    async def process_asyncio_queue_specific(self):
        print(f"Start processing data of {self.stream_id2} ...")
        while True:
            data = await self.ubwa.get_stream_data_from_asyncio_queue(self.stream_id2)
            #print(data)
            self.ubwa.asyncio_queue_task_done(self.stream_id2)

    def processing_of_stream_signals(self, signal_type=None, stream_id=None, data_record=None, error_msg=None):
        print(f"Received STREAM SIGNAL for stream '{self.ubwa.get_stream_label(stream_id=stream_id)}': "
              f"{signal_type} - {stream_id} - {data_record} - {error_msg}")

    async def start(self):
        self.stream_id1 = self.ubwa.create_stream(stream_label="stream_1", channels=['depth5'], markets=['btcusdt'])
        self.stream_id2 = self.ubwa.create_stream(stream_label="stream_2", channels=['trade'], markets=['btcusdt'],
                                                  process_asyncio_queue=self.process_asyncio_queue_specific)
        self.ubwa.create_stream(markets='arr', channels='!userData',
                                api_key="api_key", api_secret="api_secret")
        while self.ubwa.is_manager_stopping() is False:
            await asyncio.sleep(1)


if __name__ == "__main__":
    bdp = BinanceDataProcessor()
    try:
        asyncio.run(bdp.start())
    except KeyboardInterrupt:
        print("Gracefully stopping ...")
        bdp.ubwa.stop_manager()
    except Exception as error_msg:
        print(f"\r\nERROR: {error_msg}")
        print("Gracefully stopping ...")
        bdp.ubwa.stop_manager()
