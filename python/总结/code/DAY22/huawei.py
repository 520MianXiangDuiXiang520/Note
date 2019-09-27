import requests
from lxml import etree


def company():
    html = etree.HTML(requests.get("http://top.zol.com.cn/compositor/57/manu_attention.html").text)
    company_xpath = '//div[@class="section clearfix"]/div[@class="rank-list brand-rank-list"]/div[@class=' \
                    '"rank-list__item clearfix"]/div[@class="rank-list__cell cell-2"]' \
                    '/div[@class="brand_logo"]/p/a/text()'
    href_xpath = company_xpath[:-6] + '@href'
    company_list = html.xpath(company_xpath)
    company_href = html.xpath(href_xpath)
    company_dict = dict(zip(company_list, company_href))
    print(company_dict)


def get_phone_url(company_url: str) -> list:
    phone_href_list = []
    html = etree.HTML(requests.get(company_url).text)
    page_num_xpath = '//span[@class="small-page-active"]/text()'
    page_num = int(html.xpath(page_num_xpath)[0][1:])
    href_path = '//div[@class="pic-mode-box"]/ul[@id="J_PicMode"]/li/h3/a/@href'
    phone_href_list += ["http://detail.zol.com.cn" + i for i in html.xpath(href_path)]
    for i in range(2, page_num + 1):
        com_url = company_url[:-5] + f'_0_1_2_0_{i}.html'
        html = etree.HTML(requests.get(com_url).text)
        phone_href_list += ["http://detail.zol.com.cn" + i for i in html.xpath(href_path)]
    return phone_href_list


def get_complete_parameter_page_url(phone_url: str) -> str:
    """
    得到完整参数页URL
    :param phone_url: 一个手机详情页URL
    :return: str
    """
    html = etree.HTML(requests.get(phone_url).text)
    complete_parameter_xpath = \
        '//div[ @class ="second-know con-1"] / div[@ class ="info-list-01"] / a[@ class ="section-more"] / @ href'
    complete_parameter_xpath2 = \
        '//div[@class="section"]/div[@class="section-content"]/a[@class="_j_MP_more section-more"]/@href'
    try:
        url = html.xpath(complete_parameter_xpath)[0]
    except IndexError:
        url = html.xpath(complete_parameter_xpath2)[0]
    return "http://detail.zol.com.cn" + url


def get_detil_parameter(com_parameter_url: str):
    """
    得到详细参数
    :param com_parameter_url:
    :return:
    """
    html = etree.HTML(requests.get(com_parameter_url).text)
    table_list = html.xpath("//table")
    for table in table_list:
        the_key = []
        the_value = []
        tr_list = table.xpath('./tr')
        for tr in range(len(tr_list)):
            if tr == 0:
                # 第一个tr是标题，只有一个td
                table_name = tr_list[tr].xpath('./td/text()')[0]
                print(table_name)
            else:
                th = tr_list[tr].xpath('./th')[0]
                td = tr_list[tr].xpath('./td')[0]
                key = th.xpath('./span/text()')
                if len(key) == 0:
                    key = th.xpath('./a/text()')
                the_key.append(key[0])


        print(dict(zip(the_key, the_value)))



# company()
# print(get_phone_url("http://detail.zol.com.cn/cell_phone_index/subcate57_1795_list_1.html"))
# for i in get_phone_url("http://detail.zol.com.cn/cell_phone_index/subcate57_35579_list_1.html"):
#     print(get_complete_parameter_page_url(i))
get_detil_parameter('http://detail.zol.com.cn/1269/1268038/param.shtml')
