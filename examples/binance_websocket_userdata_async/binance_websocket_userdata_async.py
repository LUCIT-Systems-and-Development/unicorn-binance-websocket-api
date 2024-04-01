from unicorn_binance_websocket_api import BinanceWebSocketApiManager
import asyncio
import logging
import os

api_key = ""
api_secret = ""
exchange = "binance.com"

logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


class BinanceDataProcessor:
    def __init__(self):
        self.db = None
        self.ubwa = BinanceWebSocketApiManager(exchange=exchange,
                                               enable_stream_signal_buffer=True,
                                               process_stream_signals=self.receive_stream_signal,
                                               output_default="UnicornFy")

    def receive_stream_signal(self, signal_type=None, stream_id=None, data_record=None, error_msg=None):
        print(f"Received stream_signal for stream '{self.ubwa.get_stream_label(stream_id=stream_id)}': "
              f"{signal_type} - {stream_id} - {data_record} - {error_msg}")

    async def process_userdata(self, stream_id=None):
        print(f"Processing data of {self.ubwa.get_stream_label(stream_id=stream_id)} ...")
        while self.ubwa.is_stop_request(stream_id=stream_id) is False:
            data = await self.ubwa.get_stream_data_from_asyncio_queue(stream_id)
            print(f"data: {data}")
            self.ubwa.asyncio_queue_task_done(stream_id)

    async def main(self):
        self.ubwa.create_stream('arr', '!userData', api_key=api_key, api_secret=api_secret,
                                process_asyncio_queue=self.process_userdata, stream_label="UD_Alice")
        await asyncio.sleep(5)
        while self.ubwa.is_manager_stopping() is False:
            self.ubwa.print_summary()
            await asyncio.sleep(600)


if __name__ == "__main__":
    bdp = BinanceDataProcessor()
    try:
        asyncio.run(bdp.main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")
    except Exception as e:
        print(f"\r\nError: {e}")
        print("Gracefully stopping ...")
    bdp.ubwa.stop_manager()
