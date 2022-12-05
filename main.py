from search import search, printMovies
from speedtest import speed_test
import pandas as pd
import argparse


# pd 控制台打印控制
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


# 初始化 argparser
parser = argparse.ArgumentParser("资源站测速工具v0.1", description="读取文件中的")
parser.add_argument("-f", default="./list.txt",
                    help="存储测试站点列表的文件地址", dest="file_path")
parser.add_argument("-n", required=True,
                    help="要搜索的影片名称", dest="name")
args = vars(parser.parse_args())


search_name = args['name']
file_lines = open(args["file_path"], "r").readlines()
print(f"正在搜索:{search_name}...")


def show_table(test_list):
    """
    打印信息
    """
    df = pd.DataFrame(test_list, columns=["资源名", "url", "资源速度(mb/s)", "资源备注"])
    df.drop('url', axis="columns", inplace=True)
    print(df)


def run():
    test_list = []  # 总的数据表
    for line in file_lines:  # 从文件中读取信息到 test_list 中
        if line == "\n":
            continue
        line = line[0:-1]
        line_list = line.split(" ")
        test_list.append([0, 0, 0, 0])
        test_list[-1][0] = line_list[0]  # name
        test_list[-1][1] = line_list[1]  # url

    for i, test_item in enumerate(test_list):
        print(f'正在测试{test_item[0]}')
        test_url = search(search_name, test_item[1])
        if test_url == "":  # 没搜索到, 跳过
            print("")
            test_list[i][2] = 0
            continue
        speed = speed_test(test_url)
        test_list[i][2] = speed
        print(f"多线程下载速度为:{round(speed,2)}MB/s\n")

    # 给速度最快的排序
    test_list.sort(key=lambda x: x[2], reverse=True)

    # print(f"序号\t资源名\t\t资源速度")
    # for index, item in enumerate(test_list):
    #     print(f"{index}\t{item[0]}\t{round(item[2],2)}MB/s")
    show_table(test_list)

    printMovies(test_list[0][1], search_name)


if __name__ == "__main__":
    run()
