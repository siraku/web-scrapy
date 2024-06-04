import requests
import os
from bs4 import BeautifulSoup

heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

url = 'https://www.ximalaya.com/yinyue/291718/'


def get_media_api(trackId):
    api_url = f'https://www.ximalaya.com/revision/play/v1/audio?id={trackId}&ptype=1'
    response = requests.get(api_url, headers=heads)
    return response.json()['data']['src']


def download(music_name, music_track_id):
    os.makedirs('./piano music', exist_ok=True)
    music_url = get_media_api(music_track_id)
    response = requests.get(music_url, headers=heads)

    with open('./piano music/' + music_name + '.mp3', mode='wb') as f:
        f.write(response.content)


def get_total_list():
    # session = requests.session()
    main_page = requests.get('https://www.ximalaya.com/yinyue/291718/', headers=heads)
    bs = BeautifulSoup(main_page.text, 'html.parser')
    result_set = bs.find_all('div', attrs={'class': 'text lF_'})
    print(result_set)
    for i in result_set:
        a = i.find('a')
        title = a.get('title').strip()
        href = a.get('href').strip()
        hrefs = href.split('/')
        trace_id = hrefs[-1]
        yield title, trace_id


if __name__ == "__main__":
    for title, trace_id in get_total_list():
        print(title+'download start')
        download(title, trace_id)
        print(title + 'download finished')
