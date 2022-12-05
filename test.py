from search import search
from speedtest import speed_test


search_string = "万圣节的新娘"

test_url = search(
    search_string, 'https://cj.lziapi.com/api.php/provide/vod/from/lzm3u8/at/xml/')
print(test_url)
speed = speed_test(test_url)
print(f"单线程下载速度为:{round(speed,2)}MB/s")
