#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests,re,json,sys,getopt
from retrying import retry
from bs4 import BeautifulSoup

def Find(string):
    # findall() 查找匹配正则表达式的字符串
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url

def main():
    urlarg="https://v.douyin.com/FSkaftB/"
    musicarg="yes"
    return urlarg,musicarg

@retry(stop_max_attempt_number=3)
def download(video_url,music_url,video_title,music_title,headers,musicarg):
    #视频下载
    if video_url == '':
        print('[  提示  ]:该视频可能无法下载哦~\r')
        return
    else:
        r=requests.get(url=video_url,headers=headers)
        if video_title == '':
            video_title = '[  提示  ]:此视频没有文案_%s\r' % music_title
        with open(f'qianqian.mp4','wb') as f:
            f.write(r.content)
            print('[  视频  ]:%s下载完成\r' % video_title)

    if music_url == '':
        print('[  提示  ]:下载出错\r')
        #return
    else:
        #原声下载
        if musicarg != 'yes':
            print('[  提示  ]:不下载%s视频原声\r' % video_title)
            #return
        else:
            r=requests.get(url=music_url,headers=headers)
            with open(f'{music_title}.mp3','wb') as f:
                f.write(r.content)
                print('[  音频  ]:%s下载完成\r' % music_title)
            #return

def video_download(urlarg,musicarg):
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
        }
        r = requests.get(url = Find(urlarg)[0])
        key = re.findall('video/(\d+)?',str(r.url))[0]
        jx_url  = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={key}'    #官方接口
        js = json.loads(requests.get(url = jx_url,headers=headers).text)

        try:
            video_url = str(js['item_list'][0]['video']['play_addr']['url_list'][0]).replace('playwm','play')   #去水印后链接
        except:
            print('[  提示  ]:视频链接获取失败\r')
            video_url = ''
        try:
            music_url = str(js['item_list'][0]['music']['play_url']['url_list'][0])
        except:
            print('[  提示  ]:该音频目前不可用\r')
            music_url = ''
        try:
            video_title = str(js['item_list'][0]['desc'])
            music_title = str(js['item_list'][0]['music']['author'])
        except:
            print('[  提示  ]:标题获取失败\r')
            video_title = '视频走丢啦~'
            music_title = '音频走丢啦~'
        download(video_url,music_url,video_title,music_title,headers,musicarg)
        # print('video_url: '+ video_url)
        # print('video_title: '+ video_title)
def get_videolis():
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
    }
    # user_url='https://v.douyin.com/FhTFvuh/'
    user_url='https://www.douyin.com/user/MS4wLjABAAAAgk2o1ME5pITu0aHQWfjSRLLKk7ej-P8D2qqN0UQXzAo?relation=0'
    resp= requests.get(url=user_url,headers=headers)
    bs=BeautifulSoup(resp.text,'html.parser')
    result_set = bs.find_all('li', attrs={'class': 'ECMy_Ztd'})

    print(result_set)


if __name__=="__main__":
    urlarg,musicarg = main()
    get_videolis()
    # video_download(urlarg,musicarg)