# Shell 常用操作

## 读取文件类

### 按行读

```shell
cat filename | while read line
do
　　echo $line
done
```