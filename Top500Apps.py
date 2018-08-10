import requests
from bs4 import BeautifulSoup as bs
import codecs
import sys
import time
import importlib
importlib.reload(sys)
import re
# -*- coding: utf-8 -*-

#去除特殊字符、空格、提取冒号或空格前的文字
def preprocessing(hotapps):
    # hotapps = ['绝地求生 刺激战场', '把它们全部砍掉', '快视频-更懂你...', '狂野飙车9：传奇', '一点金库理财...', '动态肖像捏脸 男生版', 'Material Gallery']
    result = []
    for app in hotapps:
        app = app.strip("...").lower()  # 去掉最后的"..." & 转为小写
        pattern = r"[\s|：|-]"  # ":" 是中文的冒号     [-()\"#/@;:<>{}`+=~|.!?,]
        if re.search(pattern, app):
            part_app = re.split(pattern, app)[0]  # "绝地求生 刺激战场"-> "绝地求生"
            newstr = re.sub(pattern, '', app)
            result.append(part_app)
            result.append(newstr)
        else:
            result.append(app)

    return result


def get_wdj():
    essential_app_url = "http://www.wandoujia.com/essential/app"
    essential_game_url = "http://www.wandoujia.com/essential/game"
    top_app_url = "http://www.wandoujia.com/top/app"
    top_game_url = "http://www.wandoujia.com/top/game"

    essential_selector = "div.app-box > ul > li > div.app-desc > a"
    top_selector = "div.app-box > ul > li.card > div.app-desc > h2 > a"

    essential_app_list = get_web_item(essential_app_url, essential_selector) #48
    essential_game_list = get_web_item(essential_game_url, essential_selector) #9
    top_app_list = get_web_item(top_app_url, top_selector) #24
    top_game_list = get_web_item(top_game_url, top_selector) #24

    result = set()
    result.update(essential_app_list)
    result.update(essential_game_list)
    result.update(top_app_list)
    result.update(top_game_list)
    #total = 93
    return result


def get_qqsj():
    #section > div > div > a.appName.ofh
    app_union_url = "http://sj.qq.com/myapp/union.htm?orgame=1&page=1"
    app_union_sel = "section > div > div > a.appName.ofh"
    app_union_list = get_web_item(app_union_url, app_union_sel) #56
    #不全
    all_app_url = "http://sj.qq.com/myapp/category.htm?orgame=1"
    all_app_sel = "li > div > div > a.name.ofh"
    all_app_list = get_web_item(all_app_url, all_app_sel) #40

    result = set()
    result.update(app_union_list)
    result.update(all_app_list) #73

    return result


#360手机助手总榜: 527
def get_zs360_download():
    #download/weekdownload rank, 49 apps/page, take 11 pages
    down_set = set()
    week_set = set()
    download_selector = "ul.iconList > li > h3 > a "
    for i in range(1,12):
        download_url = "http://zhushou.360.cn/list/index/cid/1/order/download/?page=" + str(i)
        download_items = get_web_item(download_url,download_selector)
        down_set.update(download_items)
        if i <= 6:
            week_url = "http://zhushou.360.cn/list/index/cid/1/order/weekdownload/?page=" + str(i)
            week_items = get_web_item(week_url,download_selector)
            week_set.update(week_items)

    result = down_set.union(week_set)
    # print(len(result))
    return result

#360手机助手下载排行榜(日/周/月）、飙升排行榜(日/周/月）、评价最高: 109
def get_zs360_hot():
    hotlist_url = "http://zhushou.360.cn/list/hotList/cid/1"
    # http://zhushou.360.cn/list/index/cid/1/order/weekdownload/?page=1
    rank_selector = "dl > dd > a.sname"
    mul_type_selector = "div.srank > ol > li > a.sname"
    rank_result = get_web_item(hotlist_url, rank_selector)
    mul_type_result = get_web_item(hotlist_url, mul_type_selector)

    result = set()
    result.update(rank_result)
    result.update(mul_type_result)

    return result

#appchina 应用汇上热门榜&人气榜
def get_appchina():
    result = set()
    selector = "td.td-app-name > span > a"
    top_url = "http://www.appchina.com/top/index.html"
    top_items = get_web_item(top_url, selector) #29
    pop_url = "http://www.appchina.com/top/popularity_index.html"
    pop_items = get_web_item(pop_url, selector)
    result.update(top_items)
    result.update(pop_items)
    return result


#anzhi 安卓应用: 15apps/page take 34
def get_anzhi():
    result = set()
    selector = "div.app_info > span > a"
    for i in range(1, 36):
        toplist_url = "http://www.anzhi.com/list_1_" + str(i) + "_hot.html"
        items = get_web_item(toplist_url, selector)
        result.update(items)
    return result


#toplist; 48apps/page; take 10 pages
def get_xiaomi():
    result = set()
    selector = "ul.applist > li > h5 > a"
    for i in range(1,14):
        download_url = "http://app.mi.com/topList?page=" + str(i)
        items = get_web_item(download_url, selector)
        result.update(items)
    return result


def get_web_item(url, selector):
    items = []
    web_data = requests.get(url)
    soup = bs(web_data.text, "html.parser")
    sel_result = soup.select(selector)
    for item in sel_result:
        items.append(item.get_text())
    return items


if __name__ == "__main__":
    start_time = time.time()

    # 360手机助手: 513
    zs360_result = get_zs360_download()
    print("360手机助手总榜: " + str(len(zs360_result)))

    # 360手机助手最新: 109
    zs360_result_hot = get_zs360_hot()
    print("360手机助手hot: " + str(len(zs360_result_hot)))

    # 应用汇 appchina : 65
    appchina_result = get_appchina()
    print("应用汇: " + str(len(appchina_result)))

    # 安智 anzhi： 504
    anzhi_result = get_anzhi()
    print("安智: " + str(len(anzhi_result)))

    # 小米应用商店 xiaomi : 507
    xiaomi_result = get_xiaomi()
    print("小米应用: " + str(len(xiaomi_result)))

    # 豌豆荚: 91
    wdj_result = get_wdj()
    print("豌豆荚: " + str(len(wdj_result)))

    # 腾讯应用宝 : 73
    qqsj_result = get_qqsj()
    print("腾讯应用宝: " + str(len(qqsj_result)))

    anzhi_360 = anzhi_result.intersection(zs360_result)
    print("anzhi_360: " + str(len(anzhi_360)))
    anzhi_mi = anzhi_result.intersection(xiaomi_result)
    print("anzhi_mi: " + str(len(anzhi_mi)))
    mi_360 = xiaomi_result.intersection(zs360_result)
    print("mi_360: " + str(len(mi_360)))


    inter_result = anzhi_360.union(anzhi_mi).union(mi_360)
    print("union of inter: " + str(len(inter_result)))
    final_result = inter_result.union(zs360_result_hot).union(appchina_result).union(wdj_result).union(qqsj_result)
    # print(final_result)
    print("final result: " + str(len(final_result)))

    # write to file
    f = codecs.open('top500apps.txt', 'w', encoding='utf-8')
    for item in final_result:
        f.write(item.strip("...") + "\n")
    f.close()
    print("--- %s seconds ---" % (time.time() - start_time))

'''
    # todo: 91助手
    # zs91_result = get_zs91()

    #todo: pp助手
    # pphelper_result = get_pphelper()
    # #appSwapUL > li.app-swap-li.log-param-f.on > ul > li:nth-child(1) > div > div > a.app-list-link > div.app-info > div.app-info-name.dot


    result = []

  


'''