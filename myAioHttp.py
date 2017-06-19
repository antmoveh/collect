import asyncio
import aiohttp


async def getPage(url, res_list):
    print(url)
    headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            assert resp.status == 200
            res_list.append(await resp.text())


class parseListPage():

    def __init__(self, page_str):
        self.page_str = page_str

    def __enter__(self):
        page_str = self.page_str

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


page_num = 5
page_url_base = 'http://blog.csdn.net/u014595019/article/list/'
page_urls = [page_url_base + str(i+1) for i in range(page_num)]
loop = asyncio.get_event_loop()
ret_list = []
tasks = [getPage(host, ret_list) for host in page_urls]
loop.run_until_complete(asyncio.wait(tasks))


articles_url = []
for ret in ret_list:
    with parseListPage(ret) as tmp:
        articles_url += tmp
ret_list = []

tasks = [getPage(url, ret_list) for url in articles_url]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
