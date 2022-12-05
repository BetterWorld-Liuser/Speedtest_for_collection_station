# 搜索用代码
# 搜索并获得集数的 dict
import json
import random
import xmltodict
import requests
import re
from requests.adapters import HTTPAdapter, Retry


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


def search(search, url):
    """
    在对应资源站进行搜索
    """

    response = {}
    try:
        response = requests.get(
            url, params={'ac': 'detail', 'wd': search}, headers=headers, timeout=5)
    except Exception as e:  # 如果发送搜索的网址是
        print("在搜索时请求超时或者遭到了拒绝🙅🏻‍♀️")
        print(e)
        return ""
    result = response.text
    decode_result = {}

    if "<!DOCTYPE html>" in result:
        print("糟糕, 爬虫被发现了!")
        return ""
    elif "xml" in url:  # 解析 xml
        decode_result = xmltodict.parse(result)
        play_str = ""  # 放影片的地址字符串 正片#...$...
        try:
            # play_str = decode_result['rss']['list']['video'][0]['dl']['dd']['#text']
            if type(decode_result['rss']['list']['video']) is list:
                play_str = decode_result['rss']['list']['video'][0]['dl']['dd']['#text']
            elif type(decode_result['rss']['list']['video']) is dict:
                play_str = decode_result['rss']['list']['video']['dl']['dd']['#text']
        except:
            print("解析 xml 失败, 可能没有搜索到")
            return ""
    else:  # 解析 json
        try:
            decode_result = json.loads(result)
            if len(decode_result['list']) == 0:
                print("没有搜索到对应影视电视剧!")
                return ""
            play_str = decode_result['list'][0]['vod_play_url']
        except:
            print("解析 JSON 失败")
            return ""

    if "m3u8" not in play_str:
        print(f"返回了云播地址:{play_str}")
        return ""
    play_str_list = play_str.split("#")
    play_dict = {}  # 备用 # 是集数和对应的 url
    for index, p in enumerate(play_str_list):
        item = re.findall(
            r'https?:\/\/[a-z|0-9|\-|.|\/|A-Z|_|:]+\.m3u8', p)
        if len(item) == 0:  # 如果匹配不到网址就跳过
            continue
        play_dict[index] = item[0]

    return random.choice(list(play_dict.items()))[1]  # 随机返回一集的m3u8地址


def printMovies(source_url, search_name):
    response = {}
    try:
        response = requests.get(
            source_url, params={'ac': 'detail', 'wd': search_name}, headers=headers, timeout=5)
    except Exception as e:  # 如果发送搜索的网址是
        print("在搜索时请求超时或者遭到了拒绝🙅🏻‍♀️")
        print(e)
        return ""
    result = response.text
    decode_result = {}

    if "<!DOCTYPE html>" in result:
        print("糟糕, 爬虫被发现了!")
        return ""
    elif "xml" in source_url:  # 解析 xml
        decode_result = xmltodict.parse(result)
        play_str = ""  # 放影片的地址字符串 正片#...$...
        try:
            # play_str = decode_result['rss']['list']['video'][0]['dl']['dd']['#text']
            if type(decode_result['rss']['list']['video']) is list:
                play_str = decode_result['rss']['list']['video'][0]['dl']['dd']['#text']
            elif type(decode_result['rss']['list']['video']) is dict:
                play_str = decode_result['rss']['list']['video']['dl']['dd']['#text']
        except:
            print("解析 xml 失败")
            return ""
    else:
        try:
            decode_result = json.loads(result)
            if len(decode_result['list']) == 0:
                print("没有搜索到对应影视电视剧!")
                return ""
            play_str = decode_result['list'][0]['vod_play_url']
        except:
            print("解析 JSON 失败")
            return ""

    if "m3u8" not in play_str:
        print(f"返回了云播地址:{play_str}")
        return ""
    play_str_list = play_str.split("#")
    play_dict = {}  # 备用 # 是集数和对应的 url
    for index, p in enumerate(play_str_list):
        item = re.findall(
            r'https?:\/\/[a-z|0-9|\-|.|\/|A-Z|_|:]+\.m3u8', p)
        if len(item) == 0:  # 如果匹配不到网址就跳过
            continue
        play_dict[index] = item[0]

    for index, item in enumerate(play_str_list):
        item_split_list = item.split("$")
        print(f"{item_split_list[0]}:{item_split_list[1]}")


if __name__ == "__main__":
    res = search(
        "财阀家的小儿子", "http://cj.ffzyapi.com/api.php/provide/vod/from/ffm3u8/at/xml/")
    print(f"输出结果:{res}")
