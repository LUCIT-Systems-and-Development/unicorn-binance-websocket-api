from unicorn_binance_websocket_api import BinanceWebSocketApiManager
import asyncio


async def main():
    async def process_asyncio_queue():
        while True:
            data = await ubwa.get_stream_data_from_asyncio_queue(stream_id)
            print(data)
            ubwa.asyncio_queue_task_done(stream_id)

    stream_id = ubwa.create_stream(channels=['trade'],
                                   markets=['ethbtc', 'btcusdt'],
                                   process_asyncio_queue=process_asyncio_queue)
    while ubwa.is_manager_stopping() is False:
        await asyncio.sleep(1)


if __name__ == "__main__":
    with BinanceWebSocketApiManager(exchange='binance.com') as ubwa:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("Gracefully stopping ...")
        except Exception as error_msg:
            print(f"\r\nERROR: {error_msg}")
            print("Gracefully stopping ...")
