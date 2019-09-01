<!--961032830987546d0e6d54829fc886f6-->

目录(Catalo)

* [lxml和xpath](#lxml%E5%92%8Cxpath)
  * [Xpath](#Xpath)
    * [Xpath节点](#Xpath%E8%8A%82%E7%82%B9)
    * [Xpath基本语法](#Xpath%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95)
    * [Xpath轴](#Xpath%E8%BD%B4)
    * [Xpath运算符](#Xpath%E8%BF%90%E7%AE%97%E7%AC%A6)
  * [lxml](#lxml)

<!--a46263f7a69f33f39fc26f907cdb773a-->
# lxml和xpath

## Xpath

XPath 是一门在 XML 文档中查找信息的语言。XPath 用于在 XML 文档中通过元素和属性进行导航。

### Xpath节点

在 XPath 中，XML 文本被处理成一棵树，有七种类型的节点：元素、属性、文本、命名空间、处理指令、注释以及文档（根）节点，节点之间存在：父，子，同胞，先辈，后代五种关系

### Xpath基本语法

|语法|作用|
|----|----|
|nodename|选取此节点的所有子节点。|
|/|从根节点选取。|
|//|从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。|
|.|选取当前节点。|
|..|选取当前节点的父节点。|
|@|选取属性。|

谓语：

|路径表达式|作用|
|---------|----|
|/a[@class='class']|从根节点选取class值为class的所有a标签|

### Xpath轴

|轴名称|结果|
|------|---|
|ancestor|选取当前节点的所有先辈（父、祖父等）。
|ancestor-or-self|选取当前节点的所有先辈（父、祖父等）以及当前节点本身。|
|attribute|选取当前节点的所有属性。|
|child|选取当前节点的所有子元素。|
|descendant|选取当前节点的所有后代元素（子、孙等）。|
|descendant-or-self|选取当前节点的所有后代元素（子、孙等）以及当前节点本身。|
|following|选取文档中当前节点的结束标签之后的所有节点。|
|following-sibling|选取当前节点之后的所有兄弟节点|
|namespace|选取当前节点的所有命名空间节点。|
|parent|选取当前节点的父节点。|
|preceding|选取文档中当前节点的开始标签之前的所有节点。|
|preceding-sibling|选取当前节点之前的所有同级节点。|
|self|选取当前节点。|
|text()|选区当前节点所有文本子节点|

推荐谷歌浏览器插件：Xpath helper

### Xpath运算符

|运算符|描述|实例|返回值|
|------|--------|------|------|
|`|`|计算两个节点集|`//book | //cd`|返回所有拥有 book 和 cd 元素的节点集|
|其他....|

## lxml

使用lxml库中的etree中的HTML方法，可以把html字符串转换为XML对象，就可以使用xpath了

```python
from lxml import etree
import requests

class QiuBaiKe:
    def __init__(self):
        self.__url=['https://www.qiushibaike.com/hot/page/{}/'.format(i) for i in range(14)]
    def _gethtml(self,url):
        html=requests.get(url).text
        element=etree.HTML(html)
        div=element.xpath('//div[@class="content"]/span/text()')
        with open('qiushi.txt','a',encoding='utf-8') as fp:
            for i in div:
                fp.write(i)
                print(i)
    def run(self):
        for i in self.__url:
            self._gethtml(i)


if __name__ == '__main__':
    qiushi=QiuBaiKe()
    qiushi.run()
```