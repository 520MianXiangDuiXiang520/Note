# eval函数

eval会接受一个字符串，并把它当作一个运算式来执行，功能比较强大，可以解析出列表，元组，字典等等类型，不过在开发中直接用eval转换用户输入结果很危险

```python
s='1+1'
eval_s=eval(s)
print(s)
print(eval_s)
```

输出

```txt
1+1
2
```

### 直接转换用户输入的后果

```python
s=eval(input("请输入..."))
print(s)
```

如果用户输入`__import__('os').system('rm -rf /*)`这个语句被eval解析后会导入os模块，调用其中的system方法，该方法会模拟终端指令....

再如有一道题：

> 纯文本文件 0021.txt, 里面的内容（包括方括号）,写入到xsl文件中

```txt
[
	[1, 82, 65535], 
	[20, 90, 13],
	[26, 809, 1024]
]
```

文件读取得到字符串，直接调用eval函数将字符串转换为列表，通过循环可以很简单的完成

```python
import xlwt

file=open('0021.txt','r',encoding='utf-8')
s=file.read()
li=eval(s)
print(li[0][1])

workbook=xlwt.Workbook()
table=workbook.add_sheet('0021')
for i in range(len(li)):
    for j in range(len(li[i])):
        table.write(i,j,li[i][j])

workbook.save('0021.xls')
```

不用eval的话可能就比较麻烦
