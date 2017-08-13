

url2 = 'https://kyfw.12306.cn/otn/leftTicket/query?purpose_codes=ADULT&leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}'
url1 = 'https://kyfw.12306.cn/otn/leftTicket/log?leftTicketDTO.train_date=2017-07-30&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT'

url2 = url2.format('2017-07-30', 'BJP', 'SHH')

import requests
# print(url2)
# r = requests.get(url1, verify=False)
# print(r.json())
# r2 = requests.get(url2, verify=False)
# print(r2.json())

