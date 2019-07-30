import requests
import json
import requests
import time
from lxml import etree
import os

# proxies = ["222.85.28.130:52590","117.191.11.80:80","117.127.16.205:8080","118.24.128.46:1080","120.78.225.5:3128","113.124.92.200:9999","183.185.1.47:9797","115.29.3.37:80","36.248.129.158:9999","222.89.32.182:9999","117.191.11.111:80","182.35.84.182:9999","47.100.103.71:80","121.63.209.92:9999","124.193.37.5:8888","39.135.24.11:8080","14.146.95.4:9797","182.35.83.244:9999","113.120.36.179:9999","1.199.31.90:9999","58.17.125.215:53281","212.64.51.13:8888","182.35.84.135:9999","163.204.247.60:9999","39.106.35.21:3128","202.39.222.32:80","120.83.111.42:9999","63.220.1.43:80","42.238.85.70:9999","117.191.11.107:80"]

headers = {
    'Cookie': 'SINAGLOBAL=9538335755646.822.1532505829725; SCF=AvPbUDu6WoemSs8mNUyrWwUmSwgU6Zg6iPaRvVTbkGKX1rbNhcnWRFLoKYuIvyod-0JDVcjv-6AgVN_tv_x9kbc.; SUHB=00xpBW_UPo9hUl; SUB=_2A25x79vSDeRhGeNI71oZ-SrPzzmIHXVTE-WarDV8PUJbkNAKLRTBkW1NSHfB70-8Ju6aPYLWWEvCI7b7bzV_f4Hd; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFvhvnF-6JhwFfQ-698_OV85JpX5oz75NHD95QfSoBR1h.Xe0BfWs4DqcjZKci39gSXPXfydntt; _s_tentry=cn.bing.com; UOR=cuiqingcai.com,widget.weibo.com,cn.bing.com; Apache=260000036604.32648.1562899406325; ULV=1562899406340:11:1:1:260000036604.32648.1562899406325:1561711888395; YF-V5-G0=95d69db6bf5dfdb71f82a9b7f3eb261a; wb_view_log_5648894345=1440*9001; wvr=6; Ugrow-G0=e1a5a1aae05361d646241e28c550f987; webim_unReadCount=%7B%22time%22%3A1564475378896%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A1%2C%22msgbox%22%3A0%7D; YF-Page-G0=aac25801fada32565f5c5e59c7bd227b|1564475390|1564475280',
}


# 当前路径+pic
pic_file_path = os.path.join(os.path.abspath(''), 'pic')

# 下载图片
def download_pic(url, nick_name):
    if not url:
        return
    if not os.path.exists(pic_file_path):
        os.mkdir(pic_file_path)
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(pic_file_path + f'/{nick_name}.jpg', 'wb') as f:
            f.write(resp.content)

# 写入留言内容
def write_comment(comment):
    comment += '\n'
    with open('comment.txt', 'a', encoding='utf-8') as f:
        f.write(comment.replace('回复', '').replace('等人', '').replace('图片评论', ''))

# 获取子评论所需参数
comment_params = {
    'ajwvr': 6,
    'more_comment': 'big',
    'is_child_comment': 'true',
    'id': '4367970740108457',
    'from': 'singleWeiBo',
    'last_child_comment_id': '',
    'root_comment_id': '',
    'root_comment_max_id': ''
}

# 获取子评论，这里只是获取了第一页的子评论信息
def get_child_comment(root_comment_id):
    comment_params['root_comment_id'] = root_comment_id
    resp = requests.get(URL, params=comment_params, headers=headers)
    resp = json.loads(resp.text)
    if resp['code'] == '100000':
        html = resp['data']['html']
        from lxml import etree
        html = etree.HTML(html)
        # 每个子评论的节点
        data = html.xpath('//div[@class="WB_text"]')
        for i in data:
            nick_name = ''.join(i.xpath('./a/text()')).strip().replace('\n', '')
            comment = ''.join(i.xpath('./text()')).strip().replace('\n', '')
            write_comment(comment)
            # 获取图片对应的html节点
            pic = i.xpath('.//a[@action-type="widget_photoview"]/@action-data')
            pic = pic[0] if pic else ''
            if pic:
                # 拼接另外两个必要参数
                pic = pic + 'ajwvr=6&uid=5648894345'
                # 构造出一个完整的图片url
                url = 'https://weibo.com/aj/photo/popview?' + pic
                resp = requests.get(url, headers=headers)
                resp = resp.json()
                if resp.get('code') == '100000':
                    # 从突然url中，第一个就是评论中的图
                    url = resp['data']['pic_list'][0]['clear_picSrc']
                    # 下载图片
                    download_pic(pic_url, nick_name)
        print("子评论抓取完毕...")




if __name__ == '__main__':
    params = {
        'ajwvr': 6,
        'id': '4367970740108457',
        'from': 'singleWeiBo',
        'root_comment_max_id': ''
    }
    URL = 'https://weibo.com/aj/v6/comment/big'
    # 爬去100页，需要代理，或者进行sleep 不然会超时。
    for num in range(101):
        print(f'=========   正在读取第 {num} 页 ====================')
        # resp = requests.get(URL, params=params, headers=headers, proxies={"http": random.choices(proxies)[0]})
        resp = requests.get(URL, params=params, headers=headers)
        resp = json.loads(resp.text)
        if resp['code'] == '100000':
            html = resp['data']['html']

            html = etree.HTML(html)
            max_id_json = html.xpath('//div[@node-type="comment_loading"]/@action-data')[0]
            from urllib.parse import parse_qs

            node_params = parse_qs(max_id_json)
            # max_id
            max_id = node_params['root_comment_max_id'][0]
            params['root_comment_max_id'] = max_id
            # data = html.xpath('//div[@class="list_ul"]/div[@node-type="root_comment"]/div[@class="list_con"]')
            data = html.xpath('//div[@node-type="root_comment"]')
            for i in data:
                # 评论人昵称
                nick_name = i.xpath('.//div[@class="WB_text"]/a/text()')[0]
                # 评论内容。
                # test = i.xpath('.//div[@class="WB_text"]/text()')
                wb_text = i.xpath('.//div[@class="WB_text"][1]/text()')
                string = ''.join(wb_text).strip().replace('\n', '')
                write_comment(string)
                # 评论id , 用于获取评论内容
                comment_id = i.xpath('./@comment_id')[0]
                # 评论的图片地址
                pic_url = i.xpath('.//li[@class="WB_pic S_bg2 bigcursor"]/img/@src')
                pic_url = 'https:' + pic_url[0] if pic_url else ''
                download_pic(pic_url, nick_name)
                # 查看评论
                get_child_comment(root_comment_id=comment_id)


