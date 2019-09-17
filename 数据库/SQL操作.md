# SQL 操作

## 检索数据 SELECT

检索数据

```sql
-- 检索单个列
SELECT 列名 FROM table_name;

-- 检索多个列
SELECT 列1, 列2 FROM table_name;

-- 检索所有列
SELECT * FROM table_name;

-- 检索不同的值
SELECT DISTINCT 列名 FROM table_name;
```

限制检索结果

```sql
-- SQL Server / Access
SELECT TOP 5 列名 FROM table_name;

-- DB2
SELECT 列名 FROM table_name FETCH FIRST 5 ROWS ONLY;

-- Oracle
SELECT prod_name FROM table_name WHERE ROWNUM <= 5;

-- MyDQL / MariaDB / PostgreSQL / SQLite
SELECT prod_name FROM table_name LIMIT 5;

-- MySQL 从第六行开始，检索五行
SELECT prod_name FROM table_name LIMIT 5 OFFSET 6;

-- MySQL 与 MariaSQL 快捷键，上一条语句等价于：
SELECT prod_name FROM table_name LIMIT 5,6
```

## 排序检索数据 ORDER BY

```sql
-- 按单个列排序，默认从小到大
SELECT field1, field2 from table_name ORDER BY field1;

-- 按多个列排序，先按第一个排，第一个相同再按第二个排
SELECT field1, field2 from table_name ORDER BY field1, field2;

-- 按列位置排序
SELECT field1, field2 from table_name ORDER BY 4,5;

-- 降序排序，与DESC相对的是ASC，但ASC是默认的，DESC只作用于他前面的那一列
SELECT field1, field2 from table_name ORDER BY field1 DESC,field2 DESC;
```

## 过滤数据 WHERE

```sql
-- ORDER BY 语句应该始终放在最后
SELECT field1, field2 FROM table_name WHERE field1 = 3;
```

WHERE操作符

|操作符|说明|
|------|---|
|=|等于|
|!=或<>|不等于|
|<（>）|小于（大于）|
|<= （》=）|小于等于（大于等于）|
|!<|不小于|
|!>|不大于|
|BETWEEN|在指定两个值之间|
|IS NULL|为NULL值|

```sql
-- 范围检查，范围需要用AND连接，包括边界
SELECT * FROM stu WHERE grade BETWEEN 70 AND 100;
+----+----------+-----+-------+---------------------+
| id | name     | sex | grade | birthday            |
+----+----------+-----+-------+---------------------+
|  1 | zhangsan | boy |    99 | 2019-09-12 19:21:31 |
|  3 | wangwu   | boy |    77 | 2019-09-03 19:22:52 |
|  4 | zhaoliu  | boy |    77 | 2019-09-10 19:28:22 |
+----+----------+-----+-------+---------------------+
3 rows in set (0.33 sec)
```

### 高级数据过滤

```sql
-- AND 操作
SELECT * FROM stu WHERE grade>90 AND sex = "boy";

-- OR 操作
SELECT * FROM stu WHERE grade > 90 OR grade < 60;

-- IN 操作
SELECT * FROM stu WHERE name IN ('zhangsan', "lisi");

-- NOT操作
SELECT * FROM stu WHERE NOT name IN ('zhangsan', "lisi");
```

* AND 操作符优先级高于OR，可以加括号改变优先级
* IN比OR执行更快
* IN可以包含其他SELECT语句
* NOT否定跟在它后面的语句

### 使用通配符进行数据过滤 LIKE

|通配符|作用|
|-----|----|
|%|匹配任何字符出现任意次|
|_|匹配单个字符|
|[]|匹配指定位置的一个字符(只有SQL Server支持)|

```sql
-- 匹配name中带有n的字段
select * from stu where name like "%n%";

-- 匹配name以z或w开头的字段（SQL Server）
select * from stu where name like "[zw]%";
```

* 通配符搜索耗时比其他搜索长，不要依赖于通配符搜索

## 创建计算字段

计算字段并不存在于数据库，只是在执行SELECT语句时生成的

### 拼接字段

|DBMS|符号|
|----|----|
|Access, SQL Server|+|
|DB2,Oracle,PostgreSQL,SQLite,Open Office Base|`||`|
|Mysql,MariaDB|使用`Concat()`函数|

```sql
-- SQL Server
SELECT name + "(" + grade + ")" FROM stu ORDER BY grade;

-- MySQL
SELECT CONCAT(name,"(",grade,")") FROM stu ORDER BY grade;
+----------------------------+
| CONCAT(name,"(",grade,")") |
+----------------------------+
| lisi(66)                   |
| wangwu(77)                 |
| zhaoliu(77)                |
| zhangsan(99)               |
+----------------------------+
```

### 使用别名

```SQL
-- SQL Server
SELECT
name + "(" + grade + ")" AS new_name
FROM stu ORDER BY grade;

-- MySQL
SELECT CONCAT(name,"(",grade,")") AS new_name
FROM stu ORDER BY grade;
+--------------+
| new_name     |
+--------------+
| lisi(66)     |
| wangwu(77)   |
| zhaoliu(77)  |
| zhangsan(99) |
+--------------+
```

### 执行算数运算

支持 +，-，*，/

```sql
SELECT * ,
grade*0.1 AS new_grade
FROM stu ORDER BY grade;
+----+----------+-----+-------+---------------------+-----------+
| id | name     | sex | grade | birthday            | new_grade |
+----+----------+-----+-------+---------------------+-----------+
|  2 | lisi     | boy |    66 | 2019-09-04 19:22:05 |       6.6 |
|  3 | wangwu   | boy |    77 | 2019-09-03 19:22:52 |       7.7 |
|  4 | zhaoliu  | boy |    77 | 2019-09-10 19:28:22 |       7.7 |
|  1 | zhangsan | boy |    99 | 2019-09-12 19:21:31 |       9.9 |
+----+----------+-----+-------+---------------------+-----------+
4 rows in set (0.00 sec)
```

## 函数

每个DBMS都支持自己特定的函数，只有少数函数被大多DBMS支持

### 数据处理函数

文本处理函数

|函数|说明|
|----|---|
|LEFT()|返回字符串左边的字符|
|RIGHT()|返回字符串右边字符|
|LENGTH()或DATALENGTH()或LEN()|返回字符串长度|
|LOWER()  Access使用LCASE()|将字符串转换为小写|
|UPPER()  Access使用UCASE()|将字符串转换为大写|
|LTRIM()|去掉字符串左边空格|
|RTRIM()|去掉字符串右边空格|
|SOUNDEX()|返回字符串的SOUNDEX值|

* soundex是判断读音是不是相同，可惜中文不行,有趣的是这个算法发明的时间比计算机发明的时间还早，哈哈哈

```sql
mysql> SELECT * FROM stu WHERE SOUNDEX(name) = SOUNDEX("enn");
+----+------+-----+-------+---------------------+
| id | name | sex | grade | birthday            |
+----+------+-----+-------+---------------------+
|  5 | en   | boy |    33 | 2019-09-29 20:41:41 |
+----+------+-----+-------+---------------------+
```

时间日期处理函数

```sql
-- SQL Server
SELECT * FROM stu WHERE DATEPART(yy, birthday) = 2012;

-- Access
SELECT * FROM stu WHERE DATEPART("yyyy", birthday) = 2012;

-- PostgreSQL
SELECT * FROM stu WHERE DATE_PART('year', birthday) = 2012;

-- Oracle
SELECT * FROM stu WHERE to_number(to_char(birthday,'yyyy')) = 2012;

-- MySQL MairiaDB
SELECT * FROM stu WHERE YEAR(birthday) = 2012;

-- SQLite
SELECT * FROM stu WHERE strftime('%Y', birthday) = 2102;
```

数值处理函数

|函数|说明|
|----|---|
|ABS()|绝对值|
|COS(),SIN(),TAN()|余弦，正弦，正切|
|PI()|圆周率|
|EXP()|指数|
|SQRT()|平方根|

### 聚集函数

SQL聚集函数

|函数|说明|
|----|---|
|AVG()|返回某列平均值|
|COUNT()|返回某列行数|
|MAX() MIN()|返回某列最大最小值|
|SUM()|返回某列之和|

* COUNT(*)对表中所有行计数，不管是否包含空值
* COUNT(列)对特定列中具有特定值的行计数，忽略空值
* 可以使用DISTINCT聚集不同的值(Access不支持)

```sql
SELECT
COUNT(*) AS count_num,
AVG(DISTINCT grade) AS avg_grade,
MAX(grade) AS max_grade,
MIN(grade) AS min_grade,
SUM(grade) AS sun_grade
FROM stu;
+-----------+-----------+-----------+-----------+-----------+
| count_num | avg_grade | max_grade | min_grade | sun_grade |
+-----------+-----------+-----------+-----------+-----------+
|         6 |   74.2000 |        99 |        33 |       448 |
+-----------+-----------+-----------+-----------+-----------+
1 row in set (0.00 sec)
```

## 分组数据 GROUP BY

```sql
select grade, count(*) AS nums from stu group by grade;
+-------+------+
| grade | nums |
+-------+------+
|    99 |    1 |
|    66 |    1 |
|    77 |    2 |
|    33 |    1 |
|    96 |    1 |
+-------+------+
5 rows in set (0.00 sec)
```
