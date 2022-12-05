from random import choices
import time
import requests
import urllib3
import random
import re
from threading import Thread, Lock

mutex = Lock()
user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                   "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                   "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                   ]

headers = {
    'User-Agent': random.choice(user_agent_list),
    'referer': "https://dianyin.babelgo.cn",
}


def task(download_url, chunk_length):
    response = {}
    try:
        response = requests.get(download_url, headers=headers, timeout=5)
    except:
        print("子线程下载 ts 失败. 可能是网络不稳定或者这个资源不行")
        return 0
    data_len = len(response.content)/1024/1024
    mutex.acquire()
    chunk_length["length"] += data_len
    mutex.release()


def speed_test(m3u8):
    urllib3.disable_warnings()
    # s = requests.Session()
    # retries = Retry(total=3,
    #                 backoff_factor=0.1,
    #                 status_forcelist=[500, 502, 503, 504])
    # s.mount('https://', HTTPAdapter(max_retries=retries))
    # s.mount('http://', HTTPAdapter(max_retries=retries))
    url = m3u8
    url_base = str.join("/", url.split("/")[0:-1])+"/"  # 相对路径
    url_domain = re.findall(
        r"https?:\/\/[a-z|0-9|\-|.|A-Z|_|:]+", url)[0]  # 绝对路径

    response = {}
    try:
        response = requests.get(url, headers=headers, timeout=5, verify=False)
    except Exception as e:
        print(f"请求m3u8文件失败嘞,请求地址是:{url}")
        return 0

    m3u8_string = response.text  # 转码
    if m3u8_string == 'file not found':
        print(" 没有找到文件呀 ")
        return 0
    m3u8_list = m3u8_string.split("\n")  # 获取每一行
    for index, item in enumerate(m3u8_list):  # 稍微检查一下文件
        if item.startswith("#EXT-X-STREAM-INF"):  # 如果要跳转到另一个m3u8 的话
            # 会出现两种情况, 相对路径和绝对路径
            line = m3u8_list[index+1]
            if line.startswith("/"):  # 如果是带/的地址
                return speed_test(url_domain+line)
            elif line.startswith("http"):  # 如果是绝对地址
                return speed_test(line)
            else:  # 如果是相对地址
                return speed_test(url_base+line)

    # ts 文件分为三种情况
    # 将以 png 结尾的改成 ts 结尾

    m3u8_url_list = list(
        filter(lambda x: x.endswith("ts"), m3u8_list))  # 获取以 ts结尾的元素
    if len(m3u8_url_list) == 0:
        print("没有 ts 文件, 源可能被加密了")
        return 0
    m3u8_test_list = choices(m3u8_url_list, k=10)  # 随机选取 10 个元素

    time_start = time.time()

    chunk_length = {"length": 0}
    thread_list = []
    for ts_item in m3u8_test_list:  # 开始测试
        download_url = ""
        if ts_item.startswith("http"):  # 如果是绝对地址的话
            download_url = ts_item
        elif ts_item.startswith("/"):  # 如果是相对 domain 的地址的话
            download_url = url_domain+ts_item
        else:
            download_url = url_base+ts_item  # 拼接
        t = Thread(target=task, args=(
            download_url, chunk_length))  # 线程守护
        thread_list.append(t)
        t.start()
    list(map(lambda x: x.join(), thread_list))

    time_cost = time.time()-time_start
    print(f'耗时:{round(time_cost,2)}s')
    speed = chunk_length["length"]/(time.time()-time_start)
    return speed


if __name__ == "__main__":
    speed = speed_test(
        "https://vod2.xmyysw.com/20221116/PFmZKffF/index.m3u8")
    print(f"多线程下载速度可达{round(speed,2)}MB/s")
