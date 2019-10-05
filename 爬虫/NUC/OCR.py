import json
import requests
import base64
from io import BytesIO
from PIL import Image
from sys import version_info

class OCR:
    def __init__(self, uname: str, pwd: str, softid: str, img):
        self._uname = uname
        self._pwd = pwd
        self._softid = softid
        self._img_path = img

    def base64_api(self):
        img = Image.open(self._img_path)
        img = img.convert('RGB')
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        if version_info.major >= 3:
            b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
        else:
            b64 = str(base64.b64encode(buffered.getvalue()))
        data = {"username": self._uname, "password": self._pwd, "softid": self._softid, "image": b64}
        result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            return result["message"]
        return ""


if __name__ == "__main__":
    img_path = "E:/桌面文件/01.jpg"
    uname = 'oop'
    pwd = '8ZwbfSBaXuu'
    softid = '3b86c023688b40fa98ed4bccef57681e'
    s = OCR(uname, pwd, softid, img_path)
    print(s.base64_api())
