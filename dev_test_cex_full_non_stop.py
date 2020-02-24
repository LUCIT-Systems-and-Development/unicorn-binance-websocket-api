#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: dev_test_cex_full_non_stop.py
#
# Part of ‘UNICORN Binance WebSocket API’
# Project website: https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api
# Documentation: https://oliver-zehentleitner.github.io/unicorn-binance-websocket-api
# PyPI: https://pypi.org/project/unicorn-binance-websocket-api/
#
# Author: Oliver Zehentleitner
#         https://about.me/oliver-zehentleitner
#
# Copyright (c) 2019, Oliver Zehentleitner
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import logging
import time
import threading
import os


def print_stream_data_from_stream_buffer(binance_websocket_api_manager):
    time.sleep(30)
    while True:
        if binance_websocket_api_manager.is_manager_stopping():
            exit(0)
        oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
        if oldest_stream_data_from_stream_buffer is False:
            time.sleep(0.01)


# https://docs.python.org/3/library/logging.html#logging-levels
logging.basicConfig(level=logging.INFO,
                    filename=os.path.basename(__file__) + '.log',
                    format="{asctime} [{levelname:8}] {process} {thread} {module}: {message}",
                    style="{")

# create instance of BinanceWebSocketApiManager
binance_websocket_api_manager = BinanceWebSocketApiManager()

print("starting monitoring api!")
binance_websocket_api_manager.start_monitoring_api()

# set api key and secret for userData stream
binance_api_key = ""
binance_api_secret = ""

binance_websocket_api_manager.set_private_api_config(binance_api_key, binance_api_secret)
userdata_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!userData"])

ticker_all_stream_id = binance_websocket_api_manager.create_stream(["!ticker"], ["arr"])
miniticker_stream_id = binance_websocket_api_manager.create_stream(["arr"], ["!miniTicker"])

channels = {'aggTrade', 'trade', 'kline_1m', 'kline_5m', 'kline_15m', 'kline_30m', 'kline_1h', 'kline_2h', 'kline_4h',
            'kline_6h', 'kline_8h', 'kline_12h', 'kline_1d', 'kline_3d', 'kline_1w', 'kline_1M', 'miniTicker',
            'ticker', 'bookTicker', 'depth5', 'depth10', 'depth20', 'depth', 'depth@100ms',
            '!miniTicker', '!ticker', '!bookTicker'}

markets = ['xrpbearbusd', 'zeceth', 'cndbtc', 'dashbtc', 'atompax', 'perlbtc', 'ardreth', 'zecbnb', 'bchabctusd',
           'usdsbusdt', 'winbnb', 'xzcxrp', 'bchusdc', 'wavesbnb', 'kavausdt', 'btsusdt', 'chzbnb', 'tusdbnb',
           'xtzbusd', 'bcptusdc', 'dogebnb', 'eosbearusdt', 'ambbnb', 'wrxbnb', 'poabtc', 'wanbtc', 'ardrbtc', 'icnbtc',
           'tusdusdt', 'atombusd', 'nxseth', 'bnbusdt', 'trxxrp', 'erdpax', 'erdbtc', 'icxbusd', 'nulsbtc', 'hotusdt',
           'wavespax', 'zilbnb', 'arnbtc', 'nulsusdt', 'wintrx', 'npxsbtc', 'busdtry', 'qtumbnb', 'eosbtc', 'xlmpax',
           'tomobnb', 'eosbnb', 'engbtc', 'linketh', 'xrpbtc', 'fetbtc', 'stratusdt', 'navbnb', 'bcneth', 'yoyobtc',
           'nanobnb', 'saltbtc', 'tfuelusdc', 'skybnb', 'fuelbtc', 'bnbusdc', 'inseth', 'btcpax', 'batbtc', 'rlceth',
           'arketh', 'ltcpax', 'ltcbusd', 'duskbtc', 'mftusdt', 'bntusdt', 'mdabtc', 'enjbtc', 'poabnb', 'nanobusd',
           'paxtusd', 'hotbtc', 'bcdbtc', 'beambnb', 'trxeth', 'omgbnb', 'cdtbtc', 'eosusdc', 'dashbusd', 'cocosbtc',
           'dasheth', 'xrptusd', 'atomtusd', 'rcneth', 'rpxeth', 'xlmusdc', 'aionbusd', 'nxsbtc', 'chateth', 'repbtc',
           'tctusdt', 'linkusdt', 'nasbtc', 'usdsusdc', 'xvgbtc', 'elfeth', 'ctxcbtc', 'cmteth', 'gnteth', 'usdspax',
           'zilbtc', 'batpax', 'stratbtc', 'xzcbtc', 'iotausdt', 'etcbnb', 'ankrusdt', 'xlmeth', 'loombtc', 'erdusdc',
           'rdnbnb', 'icneth', 'vetbtc', 'cvcusdt', 'ftmpax', 'ethbullusdt', 'edoeth', 'steemeth', 'gobnb', 'hsrbtc',
           'ambbtc', 'bchabcbtc', 'dntbtc', 'btctusd', 'denteth', 'snglsbtc', 'eosbullusdt', 'xlmtusd', 'tnteth',
           'sysbnb', 'renusdt', 'zrxusdt', 'xlmbtc', 'stormbtc', 'ncashbnb', 'omgusdt', 'troyusdt', 'venbtc', 'modbtc',
           'dogepax', 'ontusdc', 'eurbusd', 'tctbnb', 'gxsbtc', 'celrbnb', 'adausdt', 'beambtc', 'elfbtc', 'celrbtc',
           'rvnusdt', 'poaeth', 'wavesusdc', 'trxbnb', 'trxusdc', 'ethbearusdt', 'ethpax', 'bateth', 'kavabtc',
           'paxbtc', 'trigbnb', 'btcusdc', 'oneusdc', 'xrptry', 'stxusdt', 'strateth', 'lendeth', 'neousdc',
           'mithusdt', 'btcngn', 'blzeth', 'evxeth', 'dnteth', 'grsbtc', 'arneth', 'iotabnb', 'waneth', 'xtzbnb',
           'subeth', 'btsbtc', 'cvceth', 'ethusdc', 'etctusd', 'cloakbtc', 'grseth', 'eospax', 'cdteth', 'bchusdt',
           'lskusdt', 'enjbusd', 'drepbtc', 'manaeth', 'tomousdt', 'algobnb', 'wtceth', 'linkpax', 'batbnb', 'sceth',
           'rvnbusd', 'cvcbnb', 'manabtc', 'gasbtc', 'stxbtc', 'cloaketh', 'neotusd', 'lrceth', 'thetabtc', 'dogeusdt',
           'aionbnb', 'viabtc', 'keyeth', 'nanoeth', 'ncasheth', 'bgbpusdc', 'ltobnb', 'snmeth', 'adabtc', 'btseth',
           'qtumbusd', 'wtcbnb', 'dcrbtc', 'fttbnb', 'paxbnb', 'insbtc', 'gntbnb', 'etheur', 'dashusdt', 'rcnbtc',
           'btcusdt', 'wanusdt', 'powrbnb', 'xmrbnb', 'trigeth', 'xzceth', 'bchbtc', 'qspbnb', 'scbnb', 'mcoeth',
           'powrbtc', 'algotusd', 'ankrbtc', 'tusdeth', 'keybtc', 'usdcusdt', 'ftmusdc', 'atombnb', 'zenbtc', 'dockbtc',
           'neobtc', 'phbbnb', 'bnbpax', 'brdbnb', 'trxusdt', 'trxbusd', 'mtlbtc', 'ftmtusd', 'perlusdc', 'mithbnb',
           'eosbullbusd', 'reqeth', 'bccbnb', 'veneth', 'loombnb', 'trxpax', 'usdcpax', 'stormusdt', 'ognbtc', 'gvtbtc',
           'iotaeth', 'naseth', 'drepusdt', 'gvteth', 'wrxusdt', 'bchabcpax', 'ongbtc', 'usdcbnb', 'dgdeth', 'salteth',
           'mtleth', 'bcnbnb', 'neblbnb', 'wanbnb', 'ontusdt', 'npxsusdt', 'mftbtc', 'eosbearbusd', 'bntbtc', 'gtoeth',
           'modeth', 'etcusdc', 'veteth', 'bcptpax', 'atomusdc', 'duskpax', 'kavabnb', 'lunbtc', 'adxbtc', 'bnteth',
           'funbtc', 'knceth', 'dogebtc', 'bchsvpax', 'bcpttusd', 'osteth', 'oaxeth', 'wabibtc', 'appcbtc', 'qkcbtc',
           'nanousdt', 'wingsbtc', 'hbarusdt', 'eurusdt', 'waveseth', 'asteth', 'linkbusd', 'btttusd', 'zecusdc',
           'bnbusds', 'linkbtc', 'venusdt', 'hotbnb', 'usdtrub', 'tctbtc', 'ankrpax', 'btctry', 'adabnb', 'polybtc',
           'bcceth', 'enjeth', 'bnbbusd', 'repbnb', 'bullusdt', 'vitebtc', 'btgbtc', 'renbtc', 'thetausdt', 'troybtc',
           'dentbtc', 'ostbtc', 'nxsbnb', 'mithbtc', 'xmrbtc', 'tomobtc', 'nulseth', 'phbbtc', 'duskbnb', 'yoyoeth',
           'ontbusd', 'btgeth', 'etcusdt', 'atomusdt', 'hcbtc', 'brdbtc', 'fttbtc', 'celrusdt', 'lskbnb', 'phbpax',
           'xtzbtc', 'batusdt', 'viteusdt', 'trxbtc', 'bchtusd', 'xtzusdt', 'ftmbtc', 'enjbnb', 'arkbtc', 'wavesusdt',
           'ftmusdt', 'neobusd', 'stormbnb', 'luneth', 'gntbtc', 'gtousdt', 'chzusdt', 'sntbtc', 'bandbnb', 'hoteth',
           'wingseth', 'mcobtc', 'docketh', 'drepbnb', 'eosusdt', 'eostusd', 'npxseth', 'thetaeth', 'iotxbtc', 'phxbnb',
           'enjusdt', 'tfuelbnb', 'mcobnb', 'ontpax', 'dcrbnb', 'batusdc', 'snglseth', 'qlcbtc', 'qspeth', 'cndeth',
           'appcbnb', 'wprbtc', 'sysbtc', 'iostusdt', 'btceur', 'mtlusdt', 'ethrub', 'tfuelpax', 'maticusdt', 'ftmbnb',
           'xrpbusd', 'iotxusdt', 'tusdbtusd', 'trigbtc', 'atombtc', 'bchpax', 'eosbusd', 'zileth', 'gtotusd',
           'xrpbullusdt', 'onetusd', 'algobtc', 'bchsvusdt', 'gtopax', 'etceth', 'vibebtc', 'bttusdt', 'repeth',
           'iostbnb', 'usdttry', 'btsbnb', 'ankrbnb', 'dltbnb', 'snteth', 'linktusd', 'nknusdt', 'rpxbtc', 'rdneth',
           'cocosusdt', 'etcbusd', 'btttrx', 'bandbtc', 'steembnb', 'zecpax', 'viabnb', 'cosbnb', 'mtheth', 'xrpusdc',
           'xemeth', 'pivxbnb', 'phxbtc', 'zilusdt', 'poeeth', 'bnbeur', 'bandusdt', 'vetbnb', 'lendbtc', 'xlmbnb',
           'duskusdt', 'mfteth', 'funusdt', 'adabusd', 'perlbnb', 'btcbusd', 'ltobtc', 'nasbnb', 'algousdt', 'zeneth',
           'bchsvusdc', 'mcousdt', 'venbnb', 'hceth', 'fetusdt', 'edobtc', 'mftbnb', 'cosusdt', 'arpausdt', 'xmrusdt',
           'ctxcusdt', 'bqxbtc', 'npxsusdc', 'icxbnb', 'bchbnb', 'phbusdc', 'tomousdc', 'nulsbnb', 'rcnbnb', 'arpabnb',
           'qtumbtc', 'keyusdt', 'agibtc', 'mblbtc', 'eoseth', 'tusdbtc', 'aioneth', 'storjbtc', 'lsketh', 'bchsvbtc',
           'bntbusd', 'ncashbtc', 'mblbnb', 'polybnb', 'aebnb', 'ltceth', 'dogeusdc', 'wpreth', 'syseth', 'bcnbtc',
           'ognusdt', 'nanobtc', 'astbtc', 'zrxeth', 'adxeth', 'gxseth', 'ethbearbusd', 'onepax', 'scbtc', 'icxbtc',
           'ontbnb', 'qlceth', 'btsbusd', 'rlcbtc', 'chatbtc', 'wabibnb', 'renbnb', 'xrpbullbusd', 'wavesbtc', 'funeth',
           'rlcbnb', 'phxeth', 'winbtc', 'storjeth', 'wavesbusd', 'iostbtc', 'icxeth', 'adatusd', 'nknbnb', 'btcrub',
           'pivxbtc', 'perlusdt', 'bullbusd', 'bttusdc', 'bcptbtc', 'aebtc', 'ethusdt', 'ltousdt', 'subbtc', 'thetabnb',
           'blzbtc', 'tfuelusdt', 'evxbtc', 'hbarbtc', 'ambeth', 'winusdt', 'qtumeth', 'dgdbtc', 'adaeth', 'busdusdt',
           'xrpbnb', 'adapax', 'usdsbusds', 'cocosbnb', 'navbtc', 'rvnbtc', 'tnbbtc', 'bnbbtc', 'neopax', 'bearusdt',
           'usdstusd', 'snmbtc', 'rvnbnb', 'gtobnb', 'phbtusd', 'hcusdt', 'btcusds', 'reqbtc', 'ognbnb', 'lrcbtc',
           'xrpeth', 'loometh', 'zectusd', 'vibeeth', 'gobtc', 'bnbtry', 'bcdeth', 'qkceth', 'neoeth', 'paxusdt',
           'bchsvtusd', 'fetbnb', 'yoyobnb', 'xlmbusd', 'skyeth', 'paxeth', 'ltcbtc', 'xvgeth', 'tnbeth', 'stratbusd',
           'agieth', 'xlmusdt', 'lskbtc', 'bearbusd', 'hsreth', 'ctxcbnb', 'oaxbtc', 'qspbtc', 'iotxeth', 'qlcbnb',
           'algousdc', 'etcpax', 'fueleth', 'aionusdt', 'xmreth', 'maticbtc', 'dashbnb', 'oneusdt', 'brdeth', 'viaeth',
           'omgeth', 'ankrtusd', 'usdsusdt', 'ethtusd', 'wavestusd', 'iosteth', 'cmtbnb', 'ostbnb', 'ltcusdt', 'ethtry',
           'zrxbtc', 'bchabcusdt', 'onebnb', 'beamusdt', 'nebleth', 'bcptbnb', 'adxbnb', 'ontbtc', 'bttbnb', 'dockusdt',
           'bccbtc', 'omgbtc', 'algopax', 'neousdt', 'xrprub', 'busdngn', 'appceth', 'dentusdt', 'xzcbnb', 'tfueltusd',
           'xembnb', 'arpabtc', 'ankrusdc', 'adausdc', 'kmdeth', 'troybnb', 'bnbeth', 'ltcusdc', 'databtc', 'blzbnb',
           'naveth', 'btcbbtc', 'battusd', 'bnbngn', 'bchbusd', 'busdrub', 'ltctusd', 'vetbusd', 'ongbnb', 'fttusdt',
           'bccusdt', 'ongusdt', 'engeth', 'usdctusd', 'etcbtc', 'gtousdc', 'mdaeth', 'vitebnb', 'erdusdt', 'dltbtc',
           'bnbtusd', 'wtcbtc', 'xrpusdt', 'xrpeur', 'agibnb', 'trxtusd', 'ethbullbusd', 'iotabtc', 'xembtc',
           'bchabcusdc', 'duskusdc', 'xrppax', 'mblusdt', 'kmdbtc', 'neblbtc', 'maticbnb', 'bnbrub', 'bcpteth',
           'bttbtc', 'stxbnb', 'dlteth', 'onteth', 'vetusdt', 'ppteth', 'ethbtc', 'onebtc', 'ethbusd', 'zecbtc',
           'erdbnb', 'xrpbearusdt', 'stratbnb', 'cmtbtc', 'cvcbtc', 'kncbtc', 'rpxbnb', 'zenbnb', 'cndbnb', 'ardrbnb',
           'bchabcbusd', 'ltcbnb', 'pivxeth', 'skybtc', 'tntbtc', 'poebtc', 'steembtc', 'icxusdt', 'tfuelbtc', 'chzbtc',
           'vibeth', 'winusdc', 'gtobtc', 'linkusdc', 'batbusd', 'rdnbtc', 'dataeth', 'bttpax', 'zrxbnb', 'vibbtc',
           'neobnb', 'cosbtc', 'powreth', 'rlcusdt', 'hbarbnb', 'wabieth', 'bqxeth', 'aionbtc', 'aeeth', 'mthbtc',
           'wrxbtc', 'pptbtc', 'nknbtc', 'zecusdt', 'stormeth', 'qtumusdt']

binance_websocket_api_manager.create_stream(["aggTrade"], markets)
binance_websocket_api_manager.create_stream(["trade"], markets)
binance_websocket_api_manager.create_stream(["kline_1m"], markets)
binance_websocket_api_manager.create_stream(["kline_5m"], markets)
binance_websocket_api_manager.create_stream(["kline_15m"], markets)
binance_websocket_api_manager.create_stream(["kline_1h"], markets)
binance_websocket_api_manager.create_stream(["kline_12h"], markets)
binance_websocket_api_manager.create_stream(["kline_1w"], markets)
binance_websocket_api_manager.create_stream(["ticker"], markets)
binance_websocket_api_manager.create_stream(["miniTicker"], markets)
binance_websocket_api_manager.create_stream(["depth"], markets)
binance_websocket_api_manager.create_stream(["depth5"], markets)
binance_websocket_api_manager.create_stream(["depth10"], markets)
binance_websocket_api_manager.create_stream(["depth20"], markets)
binance_websocket_api_manager.create_stream(["aggTrade"], markets)

id = binance_websocket_api_manager.create_stream(channels, markets)

# start a worker process to move the received stream_data from the stream_buffer to a print function
worker_thread = threading.Thread(target=print_stream_data_from_stream_buffer, args=(binance_websocket_api_manager,))
worker_thread.start()

# show an overview
while True:
    binance_websocket_api_manager.print_summary()
    time.sleep(1)
    #print(str(binance_websocket_api_manager.get_stream_info(id)))
    #binance_websocket_api_manager.print_stream_info(id)
    #time.sleep(2)
