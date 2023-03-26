from unicorn_binance_websocket_api.manager import BinanceWebSocketApiManager
import logging
import os
import time


logging.getLogger("unicorn_binance_websocket_api")
logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")


def callback_func(stream_data):
    print(stream_data)


ubwa = BinanceWebSocketApiManager(debug=True)
ubwa.print_summary()
stream_id = ubwa.create_stream('depth20@1000ms', 'BNBBUSD', output='dict', process_stream_data=callback_func)
time.sleep(5)
stopped = ubwa.stop_stream(stream_id)
ubwa.wait_till_stream_has_stopped(stream_id)
ubwa.print_summary()
deleted = ubwa.delete_stream_from_stream_list(stream_id)
ubwa.stop_manager_with_all_streams()
