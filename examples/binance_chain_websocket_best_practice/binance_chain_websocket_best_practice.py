#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ¯\_(ツ)_/¯

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
    def __init__(self, print_new_data=False, print_stream_signals=True, start_public=True, start_userdata=True):
        self.dex_user_address = "tbnb1unxhf8fat985ksajatfa5jea58j2kzg7mfy0e7"
        self.example_database = []
        self.print_new_data = print_new_data
        self.print_stream_signals = print_stream_signals
        self.start_public = start_public
        self.start_userdata = start_userdata
        self.ubwa = BinanceWebSocketApiManager(exchange='binance.org',
                                               auto_data_cleanup_stopped_streams=True,
                                               enable_stream_signal_buffer=True,
                                               output_default='dict',
                                               process_stream_signals=self.receive_stream_signal)

    async def main(self):
        if self.start_public is True:
            self.ubwa.create_stream(channels="allMiniTickers",
                                    markets="$all",
                                    process_asyncio_queue=self.processing_of_new_data,
                                    stream_label="public")

        if self.start_userdata is True:
            self.ubwa.create_stream(channels=['orders', 'transfers'], markets=self.dex_user_address,
                                    process_asyncio_queue=self.processing_of_new_data,
                                    stream_label="userData")

        while self.ubwa.is_manager_stopping() is False:
            await asyncio.sleep(1)
            stream_info = \
                {'public': self.ubwa.get_stream_info(stream_id=self.ubwa.get_stream_id_by_label('public')),
                 'userData': self.ubwa.get_stream_info(stream_id=self.ubwa.get_stream_id_by_label('userData'))}
            status_text = ""
            if self.start_public is True:
                status_text += (f"\tStream 'public' is {stream_info['public']['status']} "
                                f"(last_stream_signal={stream_info['public']['last_stream_signal']})\r\n")
            if self.start_userdata is True:
                status_text += (f"\tStream 'userData' is {stream_info['userData']['status']} "
                                f"(last_stream_signal={stream_info['userData']['last_stream_signal']})\r\n")
            print(f"Status:\r\n\tStored {len(self.example_database)} data records in `self.example_database`\r\n"
                  f"{status_text}")

    async def processing_of_new_data(self, stream_id=None):
        print(f"Saving the data from stream {self.ubwa.get_stream_label(stream_id=stream_id)} to the database ...")
        while self.ubwa.is_stop_request(stream_id=stream_id) is False:
            data = await self.ubwa.get_stream_data_from_asyncio_queue(stream_id)
            self.example_database.append(data)
            if self.print_new_data is True:
                print(f"Data record received and added to the database: {data}")
            self.ubwa.asyncio_queue_task_done(stream_id)

    def receive_stream_signal(self, signal_type=None, stream_id=None, data_record=None, error_msg=None):
        # More info about `stream_signals`:
        # https://github.com/LUCIT-Systems-and-Development/unicorn-binance-websocket-api/wiki/%60stream_signals%60
        if self.print_stream_signals is True:
            print(f"Received stream_signal for stream '{self.ubwa.get_stream_label(stream_id=stream_id)}': "
                  f"{signal_type} - {stream_id} - {data_record} - {error_msg}")


if __name__ == "__main__":
    bdp = BinanceDataProcessor(print_new_data=True,
                               print_stream_signals=True,
                               start_public=True,
                               start_userdata=True)
    try:
        asyncio.run(bdp.main())
    except KeyboardInterrupt:
        print("\r\nGracefully stopping ...")
    except Exception as e:
        print(f"\r\nERROR: {e}")
        print("Gracefully stopping ...")
    bdp.ubwa.stop_manager()
