import requests
import time
import json
from lxml import etree

base_url = 'https://icons8.com/preloaders/en/filtered-search/all/free'
base_interval = 0.5
# image: id
# size: 宽, 高
# image_type: 1 表示 apng, png 为 0, svg 为 2
download_url = '''
https://icons8.com/preloaders/generator.php?image={}&
speed=9&fore_color=000000&back_color=FFFFFF&size={}x{}&
transparency=0&reverse=0&orig_colors=0&gray_transp=0&
image_type=1&inverse=0&flip=0&frames_amount={}&
word=237-261-157-41-266-237-41-257-237-266-57-41-227-41-36-36-36&
download
'''.replace('\n', '')

# 1. fetch

def fetch(url, idx):
    url = base_url + url
    response = requests.get(url)
    with open('htmls/{}.html'.format(idx), 'w+') as f:
        f.write(response.text)

def fetch_all():
    fetch('', 1)
    for i in range(2, 22):
        fetch('/' + str(i), i)
        time.sleep(base_interval)

# 2. parse
def parse(html):
    nodes = html.xpath('//div[@class="preloaders-cards"]/div')
    res = []
    for node in nodes:
        _id = node.attrib.get('data-preloader-id')
        frame = node.xpath('.//div[@class="preloader__frames"]/text()')[0].split(' ')[0]
        size = node.xpath('.//div[@class="preloader__size"]/text()')[0].split('×')
        res.append({'id': _id, 'frame': int(frame), 'size': [int(size[0]), int(size[1])]})
    return res

def parse_all():
    res = []
    for i in range(1, 22):
        with open('htmls/{}.html'.format(i)) as f:
            html = etree.HTML(f.read())
            res += parse(html)
    with open('meta.json', 'w+') as f:
        f.write(json.dumps(res))

def download(image_id, width, height, frames_count):
    url = download_url.format(image_id, width, height, frames_count)
    dest = 'image/{}.png'.format(image_id)
    response = requests.get(url)
    with open(dest, 'wb+') as f:
        f.write(response.content)

def download_all():
    meta = None
    with open('meta.json', 'r') as f:
        meta = f.read()
    meta = json.loads(meta)
    for image_meta in meta:
        _id = image_meta['id']
        size = image_meta['size']
        frame = image_meta['frame']
        download(_id, size[0], size[1], frame)
        time.sleep(base_interval)

download_all()

# f = open('htmls/1.json', 'w+')
# data = json.dumps([{'name': 'steve', 'id': 1}, {'name': 'csd', 'id': 2}])
