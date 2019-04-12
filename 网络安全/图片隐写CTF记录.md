# 图片隐写CTF记录

## 工具使用

* WinHEX:一般用来修复图片，添加图片头时点 Edit > paste Zero Bitys
* StegSolve:用来查看图片的一些隐藏信息
* MP3Steago：用来分析mp3中的隐藏信息，把要分析的MP3文件放在dexode.exe的同级目录下，运行`Decode.exe -X music.mp3 -P simctf` -P后面是密码
* steghide:
  * `steghide info test.jpg` 查看图片隐藏信息
  * `steghide extract -sf test.jpg `分离图片隐藏信息
* binwalk：用来查看图片是否有附加的文件或压缩包之类的，加参数e可以分离
* bftools:用于处理Brainfuck和相关
  * `bftools.exe decode braincopter doge.jpg -o dogout.jpg`
  * `bftools.exe run -- dogout.jpg`
* Wbstego:用来处理LSB（最低位题目），decode之后用WinHex直接查看

## 几个例子

[1.九连环]( http://ctf5.shiyanbar.com/stega/huan/123456cry.jpg)
首先下载图片，在Linux上用binwalk查看发现存在一个压缩包，分离

```shell
junbao@ubuntu:~/Desktop$ binwalk -e 123456cry.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
19560         0x4C68          Zip archive data, at least v1.0 to extract, name: asd/
48454         0xBD46          Zip archive data, at least v1.0 to extract, compressed size: 184, uncompressed size: 184, name: asd/qwe.zip
48657         0xBE11          End of Zip archive
48962         0xBF42          End of Zip archive

junbao@ubuntu:~/Desktop$ cd _123456cry.jpg.extracted/
junbao@ubuntu:~/Desktop/_123456cry.jpg.extracted$ ls -h
4C68.zip  asd
junbao@ubuntu:~/Desktop/_123456cry.jpg.extracted$ tree
.
├── 4C68.zip
└── asd
    ├── good-已合并.jpg
    └── qwe.zip

1 directory, 3 files

```

发现里面有一个4c68的压缩包和一个asd的目录，asd里面又有一张图片和一个压缩包

```shell
junbao@ubuntu:~/Desktop/_123456cry.jpg.extracted/asd$ ls -lh
总用量 4.0K
-rw-r--r-- 1 junbao junbao   0 10月 19  2017 good-已合并.jpg
-rw-r--r-- 1 junbao junbao 184 10月 19  2017 qwe.zip

```

但这个图片大小是0，估计没用，打开4C68的压缩包后发现里面也有一张good-已合并.jpg和一个压缩包，那个压缩包里有一个flag.txt的文件，应该就是我们要找的，但问题是无论哪个解压都需要密码，不过还好，比较幸运，第一个压缩包密码其实是个伪密码，在Linux里直接提取就ok。

```shell
junbao@ubuntu:~/Desktop/_123456cry.jpg.extracted$ tree
.
├── 4C68
│   └── asd
│       ├── good-已合并.jpg
│       └── qwe.zip
├── 4C68.zip
└── asd
    ├── good-已合并.jpg
    └── qwe.zip

3 directories, 5 files

```

提取之后就是这样，这个图片就不是0kb了，应该隐藏这下面的压缩包密码。用steghide检查后确实隐藏一个文本文件ko.txt

```shell
junbao@ubuntu:~/Desktop/_123456cry.jpg.extracted/4C68/asd$ steghide info good-已合并.jpg
"good-已合并.jpg":
  format: jpeg
  capacity: 1.2 KB
Try to get information about embedded data ? (y/n) y
Enter passphrase:
  embedded file "ko.txt":
    size: 48.0 Byte
    encrypted: rijndael-128, cbc
    compressed: yes

```

提取出来，又要求输入密码，作者良心，密码为空

```shell
junbao@ubuntu:~/Desktop/_123456cry.jpg.extracted/4C68/asd$ steghide extract -sf good-已 合并.jpg 
Enter passphrase: 
wrote extracted data to "ko.txt".

```

拿到ko.txt,查看一下,上面应该是中文，在vi中出了编码问题，下面的应该就是密码了，其实直接在图形界面用文件管理器查看上面的乱码是 “当你看到这些就是密码了”，用这个密码解压qwe.zip里的flag.txt就能拿到flag了

```shell
¿´µ½Õâ¸öÍ¼Æ¬¾ÍÊÇÑ¹Ëõ°üµÄÃÜÂë£º^M
bV1g6t5wZDJif^J7
```

```shell
junbao@ubuntu:~/Desktop/_123456cry.jpg.extracted/4C68/asd$ unzip qwe.zip 
Archive:  qwe.zip
[qwe.zip] flag.txt password:
 extracting: flag.txt
junbao@ubuntu:~/Desktop/_123456cry.jpg.extracted/4C68/asd$ cat flag.txt 
flag{**************}
junbao@ubuntu:~/Desktop/_123456cry.jpg.extracted/4C68/asd$ 

```

[2.心中无码](http://ctf5.shiyanbar.com/stega/Lena.png)
这道题的脑洞服了

上来一张中间涂黄的美女照，用各种方法各种工具都试了没啥用，但在stegsolve中蓝色通道最低位时发现黑白相间的样子，感觉有猫腻，很明显中间大块黄色区域是干扰的，用python编程时直接过滤掉。下面是python代码

```python
from PIL import Image,ImageFont,ImageDraw
import math

imc=Image.open('E:/桌面文件/安全/Lena.png')
cor=[]
h,w=imc.size
for x in range(h):
    for y in range(w):
        # 直接过滤黄色干扰
        if imc.getpixel((x,y))!=(255,255,0):
            if imc.getpixel((x,y))[2] & 0x01:
                cor.append(0)
            else:
                cor.append(1)

width=int(math.sqrt(len(cor)))
print(width)
num=0
newimg = Image.new('RGB', (width, width))
for i in range(int(width)):
    for j in range(int(width)):
        if cor[num]==0:
            newimg.putpixel((i,j),(0,0,0))
        else:
            newimg.putpixel((i, j), (255, 255, 255))
        num+=1
newimg.save('new.jpg')
newimg.show()


```

保存是个二维码，扫码得到base64加密的数据，解密就ok

[3.LSB](http://ctf5.shiyanbar.com/stega/nvshen.jpg)

很明显，LSB，用Wbstego解码，保存得到一个`._is`文件，在WinHex中查看直接得到flag

[4.BrainFuck](http://ctf5.shiyanbar.com/stega/doge.jpg)

BrainFuck是啥，看这名字就欠揍，他估计是为了为难程序员设计的语言把，还好有工具，直接用bftools，得到一个base64的序列，解码就ok