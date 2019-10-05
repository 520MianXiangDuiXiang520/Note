import requests
from lxml import etree
from urllib import request
from NUC_INFO.GetByXpath import GetInfo
from NUC_INFO.OCR import OCR
from NUC_INFO.Setting import Setting
from NUC_INFO.SaveDataBase import SaveDataBase
from time import sleep


class Login:
    def __init__(self):
        self._get_by_xpath = GetInfo()
        self._save_data_base = SaveDataBase()
        self._ocr = OCR(
            Setting.OCR_USER_SETTING['uname'],
            Setting.OCR_USER_SETTING['pwd'],
            Setting.OCR_USER_SETTING['softid'],
            "./01.jpg"
        )
        self._code_url = 'http://202.207.177.39:8089/validateCodeAction.do?random=0'
        self._login_url = 'http://202.207.177.39:8089/loginAction.do'
        self._url = 'http://202.207.177.39:8089/xjInfoAction.do?oper=xjxx'
        self._img_url = 'http://202.207.177.39:8089/xjInfoAction.do?oper=img'

    def _download_validate_code(self):
        reques = request.Request(self._code_url, headers=Setting.HEADER_POOL['headers2'])
        re = request.urlopen(reques)
        with open('01.jpg', 'wb') as fp:
            fp.write(re.read())

    def _login(self, stu_id: str):
        self._download_validate_code()
        vcode = self._ocr.base64_api()
        print(vcode)
        data = Setting.POST_DATA_DICT
        data['zjh'] = str(stu_id)
        data['mm'] = str(stu_id)
        data['v_yzm'] = str(vcode)
        session = requests.Session()
        session.post(self._login_url, data, headers=Setting.HEADER_POOL['headers2'])
        resp = session.get(self._url, headers=Setting.HEADER_POOL['headers3'])
        re = session.get(self._img_url, headers=Setting.HEADER_POOL['headers3'])
        with open(f'{Setting.IMAGE_SAVE_PATH}/{stu_id}.{Setting.IMAGE_SAVE_TYPE}', 'wb') as fp:
            fp.write(re.content)
        html = etree.HTML(resp.text)
        sleep(Setting.SLEEP_TIME)
        return html

    def clean_data(self, stu_id):
        document = self._login(stu_id)
        try:
            stu_dict = self._get_by_xpath.get_info(document)
        except IndexError:
            # 验证码错误或数据库繁忙可能抛出次异常
            print("第一次错误，将延时")
            sleep(Setting.SLEEP_TIME)
            document = self._login(stu_id)
            try:
                stu_dict = self._get_by_xpath.get_info(document)
            except IndexError:
                print("第2次错误，将延时")
                sleep(Setting.SLEEP_TIME)
                document = self._login(stu_id)
                try:
                    print("第3次错误，将延时")
                    stu_dict = self._get_by_xpath.get_info(document)
                except IndexError:
                    print(f"{stu_id}失败！！！")
        try:
            self._save_data_base.save(stu_dict)
            print(stu_dict['name'])
        except:
            print("写入数据库失败")


if __name__ == '__main__':
    n = Login()
    stu_id = input("请输入学号：")
    n.clean_data(stu_id)
