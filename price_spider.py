import requests
from urllib.request import urlretrieve
import re
import pytesseract
from PIL import Image
from lxml import etree
import image_ocr

# 请求的url
url = "http://sz.ziroom.com/x/794177397.html"

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    }


response = requests.get(url, headers=headers)

html = etree.HTML(response.text)
bg_img_info = html.xpath('//div[@class="Z_price"]/i[@class="num"]/@style')[0]
if len(re.findall(r'background-image: url\((.*?)\)',bg_img_info)) > 0:
    bg_img_url = "http:" + re.findall(r'background-image: url\((.*?)\)',bg_img_info)[0]
    info = html.xpath('//div[@class="Z_list-box"]/div[@class="item"]')
    for i in info:
        titles = i.xpath('.//h5/a/text()')
        if titles:
            title = titles[0]
        position_list = [re.findall(r'background-position: -(.*?)px',j)[0] for j in i.xpath('.//div[@class="price "]/span[@class="num"]/@style')]
        price_list = [int(float(i)/21.4 + 1) for i in position_list]
        text = image_ocr.image_ocr(bg_img_url)
        num = [i for i in text]
        price = "￥" + "".join([num[i-1] for i in price_list]) + "/月起"
        print(title, price)
else:
      print("提取背景图片链接出错！")