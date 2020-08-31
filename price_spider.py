import requests
import re
from lxml import etree
import image_ocr

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    }
prices = []
count = 0
def get_price(urls):
    for i in urls:
        response = requests.get(i, headers=headers)
        html = etree.HTML(response.text)
        bg_img_info = html.xpath('//div[@class="Z_price"]/i[@class="num"]/@style')
        if len(re.findall(r'background-image: url\((.*?)\)',bg_img_info[0])) > 0:
            bg_img_url = "http:" + re.findall(r'background-image: url\((.*?)\)',bg_img_info[0])[0]
            position_list = []
            text = image_ocr.image_ocr(bg_img_url)
            price_list = []
            for i in bg_img_info:
                position = re.findall(r'background-position:-(.*?)px',i)[0]
                position_list.append(position)
            for i in position_list:
                price_list.append(int(float(i)/30 + 1))

            num = [i for i in text]
            price = "￥" + "".join([num[i-1] for i in price_list]) + "/月起"
            prices.append(price)
            global count
            count = count + 1
            print("提取第"+str(count)+"个价格成功")
        else:
            print("提取背景图片链接出错！")

    return prices