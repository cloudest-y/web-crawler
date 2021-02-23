# coding: utf-8

import re
import json
import requests
from threading import Timer
import time

# 基于 m.weibo.cn 抓取少量数据，无需登陆验证
url_template = "https://m.weibo.cn/api/container/getIndex?type=wb&queryVal={}&containerid=100103type=2%26q%3D{}&page={}"
# url_template = "https://s.weibo.com/weibo?q={}&typeall=1&suball=1&timescope=custom:{}:{}&Refer=g&page={}"


def clean_text(text):
    """清除文本中的表情信息"""
    text = re.sub('["\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"]', '', text)
    text = re.sub(r"\[\S+\]", "", text)
    # """合并空格，！。"""
    # text = re.sub(" +", " ", text)   # 合并空格
    # text = re.sub("[...|…|。。。]+", "...", text) # 合并句号
    # text = re.sub("!+!", "!", text)   # 合并叹号
    # text = re.sub("！+！", "！", text)   # 合并叹号
    # text = re.sub("？+？", "？", text)   # 合并问号
    # text = re.sub("?+?", "?", text)   # 合并问号
    text = text.replace(" ...全文", "") 
    """清除文本中的标签等信息"""
    dr = re.compile(r'(<)[^>]+>', re.S)
    dd = dr.sub('', text)
    dr = re.compile(r'#[^#]+#', re.S)
    dd = dr.sub('', dd)
    dr = re.compile(r'@[^ ]+ ', re.S)
    dd = dr.sub('', dd)
    
    
    return dd.strip()


def fetch_data(query_val, page_id):
    """抓取关键词某一页的数据"""
    resp = requests.get(url_template.format(query_val, query_val, page_id))
    card_group = json.loads(resp.text)['data']['cards'][0]['card_group']
    print('url：', resp.url, ' --- 条数:', len(card_group))

    mblogs = []  # 保存处理过的微博
    for card in card_group:
        mblog = card['mblog']
        # blog = {'mid': mblog['id'],  # 微博id
        #         'text': clean_text(mblog['text']),  # 文本
        #         'userid': str(mblog['user']['id']),  # 用户id
        #         'username': mblog['user']['screen_name'],  # 用户名
        #         'reposts_count': mblog['reposts_count'],  # 转发
        #         'comments_count': mblog['comments_count'],  # 评论
        #         'attitudes_count': mblog['attitudes_count']  # 点赞
        #         }
        blog = {
                'text': clean_text(mblog['text'])
                }
        mblogs.append(blog)
    return mblogs


def remove_duplication(mblogs):
    """根据微博的id对微博进行去重"""
    mid_set = {mblogs[0]['mid']}
    new_blogs = []
    for blog in mblogs[1:]:
        if blog['mid'] not in mid_set:
            new_blogs.append(blog)
            mid_set.add(blog['mid'])
    return new_blogs

def sleep_time(hour, min, sec):
    st = hour*3600 + min*60 + sec
    return st

def fetch_pages(query_val, page_num):
    """抓取关键词多页的数据"""
    mblogs = []
    for page_id in range(1 + page_num + 1):
        try:
            mblogs.extend(fetch_data(query_val, page_id))
        except Exception as e:
            print(e)

    print("去重前：", len(mblogs))
    # mblogs = remove_duplication(mblogs)
    # print("去重后：", len(mblogs))

    # 保存到 result.json 文件中
    fp = open('result_{}.json'.format(query_val), 'w', encoding='utf-8')
    json.dump(mblogs, fp, ensure_ascii=False, indent=4)
    print("已保存至 result_{}.json".format(query_val))



if __name__ == '__main__':
    "吃瓜",
    sem = ["安利","沙雕","秀",
           "真香","土味","鸽子","套娃",
           "方","狼人","佛系","凉",
           "拔草","韭菜","奶狗","种草",
           "辣鸡","稳","锦鲤","锁"]
    bln = ["awsl","duck不必","gkd","u1s1",      
           "xswl","奥里给","恰饭","口区",
           "社畜","上头","整活","打call",
           "有矿","狼灭","杠精","单身狗",
           "嗑cp","戏精","舔狗","yyds"]
    minute = sleep_time(0,10,0)
    # ii = 0
    # for item in sem:
          
    #     fetch_pages(item,60)
    #     ii = ii+1
    #     if (ii % 2) == 0:
    #         time.sleep(minute)


    # fetch_pages('杠精', 10)
    # fetch_pages('单身狗', 10)

    # time.sleep(minute)
    fetch_pages('肝', 30)
    fetch_pages('酸', 30)

    time.sleep(minute)
    # fetch_pages('锁', 10)
    # fetch_pages('辣鸡', 10)
