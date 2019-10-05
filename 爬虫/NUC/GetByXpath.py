class GetInfo:
    xpath_list = {
        'name_xpath': '//tr[@class="odd"]/td[4]/text()',
        'id_xpath': '//tr[@class="odd"]/td[2]/text()',
        'idcode_xpath': '/html/body/table[4]/tr'
                        '/td/table[1]/tr[2]/td[2]/table/tr/td/table/tr[3]/td[4]/text()',
        'sex_xpath': '/html/body/table[4]/tr'
                     '/td/table[1]/tr[2]/td[2]/table/tr/td/table/tr[4]/td[2]/text()',
        'place_xpath': '/html/body/table[4]/tr'
                       '/td/table[1]/tr[2]/td[2]/table/tr/td/table/tr[6]/td[4]/text()',
        'highschool_xpath': '/html/body/table[4]/tr'
                            '/td/table[1]/tr[2]/td[2]/table/tr/td/table/tr[8]/td[4]/text()',
        'gkid_xpath': '/html/body/table[4]/tr'
                      '/td/table[1]/tr[2]/td[2]/table/tr/td/table/tr[10]/td[2]/text()',
        'mingzu_xpath': '/html/body/table[4]/tr'
                        '/td/table[1]/tr[2]/td[2]/table/tr/td/table/tr[6]/td[2]/text()'
    }

    @staticmethod
    def get_info(html):
        args = {}
        for i in GetInfo.xpath_list:
            s = str(html.xpath(GetInfo.xpath_list[i])[0]).strip("\t\n\r ")
            s = s.replace(u'\xa0', u' ')
            args.setdefault(str(i).split('_')[0], s)
        return args
