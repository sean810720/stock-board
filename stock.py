'''
[ 台股即時行情 ]
即時從 Yahoo 股市抓上市/櫃成量排行
'''

import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import date as da
import time
import prettytable as pt
import os
from colorama import init, Fore, Back
import platform


def stock(market_no='1', choose='1'):

    try:

        # 條件初始化
        market = {
            'code': 'tse',
            'title': '上市',
            'type': 'vol',
            'type_title': '成量'
        }

        # 根據選擇變更條件
        if market_no == '2':
            market['code'] = 'otc'
            market['title'] = '上櫃'

        if choose == '2':
            market['type'] = 'pri'
            market['type_title'] = '成值'

        # 證交所 - 休市日
        # tse_holiday_url = 'https://www.twse.com.tw/zh/holidaySchedule/holidaySchedule'

        # Yahoo 股市 - 成量排行
        yahoo_stock_url = 'https://tw.stock.yahoo.com/d/i/rank.php?t={}&e={}'.format(
            market['type'], market['code'])

        # 當日開盤時間
        open_time = dt.strptime(dt.now().strftime(
            "%Y/%m/%d") + " 09:00:00", "%Y/%m/%d %H:%M:%S")

        # 當日收盤時間
        close_time = dt.strptime(dt.now().strftime(
            "%Y/%m/%d") + " 13:30:00", "%Y/%m/%d %H:%M:%S")

        # 是否收盤
        market_close = False

        while market_close == False:

            # 取得網頁內容
            rs = requests.get(yahoo_stock_url)

            # 解析網頁內容
            soup = BeautifulSoup(rs.text, 'html.parser')

            # 找出所有放在 table 元素中的資料
            result = soup.find_all('table')

            # 取資料格式檢查用
            i = 0

            # 表單初始化
            tb = pt.PrettyTable()
            tb.field_names = ['名次', '股票代號/名稱', '成交價',
                              '漲跌', '漲跌幅', '最高', '最低', '價差', '成交量(張)']

            # 只抓有股價資料的 table
            for item in result[2].find_all('tr'):

                # 只取需要的部分
                if i > 2:
                    tmp = item.find_all('td')
                    index = tmp[0].text
                    title = tmp[1].text
                    price = tmp[2].text
                    updown = tmp[3].text
                    updown_percent = tmp[4].text
                    high_price = tmp[5].text
                    low_price = tmp[6].text
                    price_margin = tmp[7].text
                    volume = Fore.LIGHTYELLOW_EX + tmp[8].text + Fore.RESET

                    # 參考價
                    reference_price = float(
                        price) - float(updown.replace('△', '').replace('▲', '').replace('▽', '-').replace('▼', '-'))

                    # 最高價調整
                    if float(high_price) > reference_price:
                        high_price = Fore.RED + high_price + Fore.RESET
                    elif float(high_price) < reference_price:
                        high_price = Fore.GREEN + high_price + Fore.RESET

                    # 最低價調整
                    if float(low_price) > reference_price:
                        low_price = Fore.RED + low_price + Fore.RESET
                    elif float(low_price) < reference_price:
                        low_price = Fore.GREEN + low_price + Fore.RESET

                    # 價格漲跌調整

                    # 漲(紅)△
                    if float(tmp[4].text[:-1]) > 0:
                        price = Fore.RED + tmp[2].text + Fore.RESET
                        updown = Fore.RED + tmp[3].text + Fore.RESET
                        updown_percent = Fore.RED + \
                            tmp[4].text + Fore.RESET

                        # 漲停 ▲
                        if updown.find('▲') > 0:
                            price = Back.RED + ' ' + \
                                tmp[2].text + ' ' + Back.RESET
                            high_price = Back.RED + ' ' + \
                                tmp[5].text + ' ' + Back.RESET

                    # 跌(綠)▽
                    elif float(tmp[4].text[:-1]) < 0:
                        price = Fore.GREEN + tmp[2].text + Fore.RESET
                        updown = Fore.GREEN + tmp[3].text + Fore.RESET
                        updown_percent = Fore.GREEN + \
                            tmp[4].text + Fore.RESET

                        # 跌停 ▼
                        if updown.find('▼') > 0:
                            price = Back.GREEN + ' ' + \
                                tmp[2].text + ' ' + Back.RESET
                            low_price = Back.GREEN + ' ' + \
                                tmp[6].text + ' ' + Back.RESET

                    # 把資料塞進表單
                    tb.add_row([index, title, price, updown,
                                updown_percent, high_price, low_price, price_margin, volume])

                # 取資料格式檢查用
                i += 1

            # 清空畫面

            # Windows
            if platform.system() == 'Windows':
                os.system('cls')

            # Linux / MacOS
            else:
                os.system('clear')

            # 時間顯示
            show_time = dt.now().strftime("%Y/%m/%d %H:%M:%S")

            # 六日
            if da.today().weekday() == 5 or da.today().weekday() == 6:
                market_close = True
                close_memo = ' (本日休市)'
                show_time = dt.now().strftime("%Y/%m/%d") + close_memo

            # 平日
            else:

                # 未開盤/收盤
                if dt.now() < open_time or dt.now() > close_time:
                    market_close = True
                    close_memo = ' (未開盤)' if dt.now(
                    ) < open_time else ' (已收盤)'
                    show_time = dt.now().strftime("%Y/%m/%d") + close_memo

            # 輸出表單
            print('\n' + market['title'] +
                  market['type_title'] + '排行: ' + show_time)
            print(tb)

            # 睡一秒
            print('[離開] Ctrl + C')
            time.sleep(1)
    except:
        pass


# 執行
market = input('\n選擇市場別 (預設為1): [1] 上市 | [2] 上櫃\n')
choose = input('\n選擇類別 (預設為1): [1] 成量排行 | [2] 成值排行\n')
stock(market, choose)
