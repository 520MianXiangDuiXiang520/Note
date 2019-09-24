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

-- MySQL / MariaDB / PostgreSQL / SQLite
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

* GROUP BY 子句可以包含任意数目的列，因此可以对分组进行嵌套，进行更细致的分组
* 如果嵌套了分组，数据将在最后指定的分组上进行汇总。（所有列一起计算）
* GROUP BY 子句中列出的每一列都必须是检索列或有效的表达式（不能是聚集函数），如果在SELECT中使用表达式，则必须在GROUP子句中指定相同的表达式，不能使用别名.
* 大多数DBMS不允许GROUP BY 带有长度可变的数据类型
* 除聚集计算语句外，SELECT语句中的每一列都必须在GROUP BY中给出
* 如果分组列中包含一个NULL值，则NULL作为一个分组返回，多个NULL作为一个分组。
* GROUP BY应该出现在WHERE之前，ORDER BY 之前。

### 过滤分组 HAVING

```sql
select grade, count(*) AS nums from stu group by grade having grade > 60;
+-------+------+
| grade | nums |
+-------+------+
|    99 |    1 |
|    66 |    1 |
|    77 |    2 |
|    96 |    1 |
+-------+------+
4 rows in set (0.10 sec)
```

> HAVING 与 WHERE 的区别：
> WHERE在数据分组前进行过滤，HAVING在数据分组后进行过滤，WHERE排除的行不包括在分组中，这可能会改变计算值，从而影响HAVING中基于这些值过滤掉的分组。
> 如果不指定GROUP BY 大多数DBMS会同等对待他们，不过，使用HAVING时应该结合GROUP BY 而WHERE应该用于标准的行级过滤。

### 分组和排序

GROUP BY　与　ORDER　BY　经常完成相同的工作，但他们非常不同，ORDER　BY　是对产生的输出进行排序，而GROUP　BY　是对行进行排序，但输出的可能不是分组的顺序，所以在使用GROUP　BY时，也应该给出ORDER　BY　子句。

```sql
--- 除ACCESS外，大部分DBMS支持用别名排序
select grade, count(*) AS nums from stu
        group by grade having grade > 60
        order by count(*);
+-------+------+
| grade | nums |
+-------+------+
|    66 |    1 |
|    96 |    1 |
|    99 |    1 |
|    77 |    2 |
+-------+------+
```

## 子查询

```sql
select * from songs where singer in  
    -> (select id from singer where name = "张靓颖");
+-----------+---------------------+--------------------------------------------------------+--------+
| id        | name                | link                                                   | singer |
+-----------+---------------------+--------------------------------------------------------+--------+
|    169794 | 天下无双            | http://music.163.com/song/media/outer/url?id=169794    |  10561 |
|    327089 | 画心                | http://music.163.com/song/media/outer/url?id=327089    |  10561 |
|    327163 | 我们说好的          | http://music.163.com/song/media/outer/url?id=327163    |  10561 |
|    327225 | 如果爱下去          | http://music.163.com/song/media/outer/url?id=327225    |  10561 |
|   5233037 | 另一个天堂          | http://music.163.com/song/media/outer/url?id=5233037   |  10561 |
|  31877130 | 饿狼传说 (Live)     | http://music.163.com/song/media/outer/url?id=31877130  |  10561 |
| 431853688 | 我的梦 (Live)       | http://music.163.com/song/media/outer/url?id=431853688 |  10561 |
+-----------+---------------------+--------------------------------------------------------+--------+
7 rows in set (0.25 sec)
```

* 子查询可以嵌套，但出于效能考虑，不应该嵌套过多。

### 作为计算字段使用子查询

```sql
mysql> SELECT name,
    -> (SELECT COUNT(*) FROM songs WHERE songs.singer = singer.id) AS nums
    -> FROM singer WHERE type IN
    -> (SELECT id FROM singer_type WHERE type = "华语男歌手")
    -> ORDER BY name
    -> LIMIT 5;
+-----------------+------+
| name            | nums |
+-----------------+------+
| “阿兰姐”        |   50 |
| 023 GC          |    0 |
| A3              |   32 |
| abduwali tohti  |    8 |
| ABSDJHONG       |   22 |
+-----------------+------+
5 rows in set (0.69 sec)
```

## 联结表

> 联结是一种机制，用来在一条SELECT语句中关联表，因此，称为联结

```sql
--- 等值联结
mysql> SELECT songs.name,link,singer.name FROM songs,singer
    -> WHERE songs.singer = singer.id
    -> LIMIT 5;
+-----------------+----------------------------------------------------+--------+
| name            | link                                               | name   |
+-----------------+----------------------------------------------------+--------+
| Happy Birth Day | http://music.163.com/song/media/outer/url?id=59867 | 阿信   |
| 几年了          | http://music.163.com/song/media/outer/url?id=59870 | 阿杜   |
| Valentines Day | http://music.163.com/song/media/outer/url?id=59875 | 阿杜   |
| 再唱一首        | http://music.163.com/song/media/outer/url?id=59877 | 阿杜   |
| 圣堂之门        | http://music.163.com/song/media/outer/url?id=59886 | 阿沁   |
+-----------------+----------------------------------------------------+--------+
5 rows in set (0.01 sec)
```

* 创建表联结时的WGERE语句非常重要，他作为过滤条件，只包含那些匹配给定条件的行，没有联结条件则会返回要联结的表的笛卡尔积（叉联结）
* 完全限定名：引用列可能出现歧义，这种情况应该使用`表名.列名`的完全限定名

### 内连接（inner-join）

上面的等值连接也叫内连接，可以显式声明联结类型

```sql
mysql> SELECT songs.name, link, singer.name AS singer
    -> FROM songs INNER JOIN singer ON
    -> songs.singer = singer.id
    -> LIMIT 5;
+-----------------+----------------------------------------------------+--------+
| name            | link                                               | singer |
+-----------------+----------------------------------------------------+--------+
| Happy Birth Day | http://music.163.com/song/media/outer/url?id=59867 | 阿信   |
| 几年了          | http://music.163.com/song/media/outer/url?id=59870 | 阿杜   |
| Valentines Day | http://music.163.com/song/media/outer/url?id=59875 | 阿杜   |
| 再唱一首        | http://music.163.com/song/media/outer/url?id=59877 | 阿杜   |
| 圣堂之门        | http://music.163.com/song/media/outer/url?id=59886 | 阿沁   |
+-----------------+----------------------------------------------------+--------+
5 rows in set (0.00 sec)
```

* SQL本身不限制联结表的数量，但许多DBMS有限制
* 联结表越多，性能下降越厉害
* 允许使用表别名(Oracle 不用 AS)

### 自联结（self-join）

```sql
mysql> SELECT s1.name,s1.singer
    -> FROM songs AS s1,songs AS s2
    -> WHERE s1.singer = s2.singer AND s2.name="光年之外";
+-----------------------------+--------+
| name                        | singer |
+-----------------------------+--------+
| 来自天堂的魔鬼              |   7763 |
| 画 (Live Piano Session II)  |   7763 |
| 光年之外                    |   7763 |
| 断讯                        | 916042 |
| 光年之外                    | 916042 |
| 那个她                      | 916042 |
+-----------------------------+--------+
6 rows in set (4.53 sec)
```

* 联结中的两张表是同一张表，必须使用别名区分。
* 许多DBMS处理自联结比处理子查询快。

### 自然联结

自然联结是一种特殊的等值联结（内联结），他要求两个关系中进行比较的分量必须是同名的属性组，并且在结果中把重复的属性列去掉，事实上，我们迄今为止建立的每个内联结都是自然联结，也很可能永远都不会用到不是自然联结的内联结。通常对一个表使用通配符（SELECT *）其他表使用明确的子集来完成。

```sql
mysql> SELECT s.* ,e.name
    -> FROM songs AS s,singer AS e
    -> WHERE s.singer = e.id AND e.name = "袁娅维";
```

### 外联结

两个关系R和S在做自然连接时，他们在公共属性上值相等的元组构成新的关系，但是关系R中某些元组可能在关系S中不存在公共属性上值相等的元组，从而造成R中的这些元组被舍弃了，同样的S中的元组也有可能被舍弃，这些被舍弃的元组被称为 **悬浮元组**

如果把悬浮元组也保存到结果关系中，而在其他属性上填空值，这种联结叫做外联结，如果只保留左边关系R中的悬浮元组就叫做左外连接，如果只保留右边关系S中的悬浮元组就叫做右外连接。

```sql
-- 原来表的数据
mysql> select * from r;
+----+----+----+
| A  | B  | C  |
+----+----+----+
| a1 | b1 | 5  |
| a1 | b2 | 6  |
| a2 | b3 | 8  |
| a2 | b4 | 12 |
+----+----+----+
4 rows in set (0.00 sec)

mysql> select * from s;
+----+----+
| B  | E  |
+----+----+
| b1 | 3  |
| b2 | 7  |
| b3 | 10 |
| b3 | 2  |
| b5 | 2  |
+----+----+
5 rows in set (0.00 sec)

-- 左外连接
mysql> SELECT r.*,s.*
    -> FROM r LEFT OUTER JOIN s
    -> ON r.b = s.b;
+----+----+----+------+------+
| A  | B  | C  | B    | E    |
+----+----+----+------+------+
| a1 | b1 | 5  | b1   | 3    |
| a1 | b2 | 6  | b2   | 7    |
| a2 | b3 | 8  | b3   | 10   |
| a2 | b3 | 8  | b3   | 2    |
| a2 | b4 | 12 | NULL | NULL |
+----+----+----+------+------+
5 rows in set (0.00 sec)

-- 右外联结
mysql> SELECT r.*,s.*
    -> FROM r RIGHT OUTER JOIN s
    -> ON r.b = s.b;
+------+------+------+----+----+
| A    | B    | C    | B  | E  |
+------+------+------+----+----+
| a1   | b1   | 5    | b1 | 3  |
| a1   | b2   | 6    | b2 | 7  |
| a2   | b3   | 8    | b3 | 10 |
| a2   | b3   | 8    | b3 | 2  |
| NULL | NULL | NULL | b5 | 2  |
+------+------+------+----+----+
5 rows in set (0.00 sec)
```

还有一种全外联结（FULL OUTER JOIN）包含两个表中不相关的行，Access，MariaDB，MySQL，Open Office Base，SQLite不支持。

### 使用带聚集函数的联结

## 组合查询 UNION

```sql
mysql> SELECT id, name from singer where name="阿沁"
    -> UNION
    -> SELECT name, id FROM singer WHERE name="林俊呈";
+-----------+----------+
| id        | name     |
+-----------+----------+
| 1872      | 阿沁     |
| 林俊呈    | 30107224 |
+-----------+----------+
2 rows in set (0.07 sec)
```

* UNION 语句中必须包含相同的列，表达式或聚集函数（次序可以不同）
* 列数据类型必须兼容
* 只能使用一条ORDER BY 语句，位于最后一个select之后
* UNION会自动删除相同的行，如果不希望这样，可以使用 UNION ALL

## 插入数据 INSERT

```sql
-- 不安全
mysql> INSERT INTO stu
    -> VALUES(
    -> 7,
    -> "dapeng",
    -> "girl",
    -> 99,
    -> "2019-10-9 10:11:21");
Query OK, 1 row affected (0.09 sec)
```

应该给出列名（虽然更加麻烦），尤其是你只打算插入部分行时。

```sql
mysql> INSERT INTO stu(id,
    ->                 name,
    ->                 sex,
    ->                 grade)
    -> VALUES(8,
    ->        "xiaowei",
    ->        "girl",
    ->        99);
Query OK, 1 row affected (0.05 sec)
```

### 插入检索出的数据

```sql
mysql> INSERT INTO stu(name,
    ->                 sex,
    ->                 grade,
    ->                 birthday)
    -> SELECT name,
    ->        sex,
    ->        grade,
    ->        birthday
    -> FROM stu WHERE id = 1;
Query OK, 1 row affected (1.67 sec)
Records: 1  Duplicates: 0  Warnings: 0
```

* 可以从本表中检索插入，也可以从其他表中检索插入。

### 从一个表复制到另一个表 SELECT INTO

* DB2 不支持

```sql
-- MariaDB,MySQL,Oracle,PostgreSQL,SQLite
mysql> CREATE TABLE s_copy AS SELECT * FROM s;
Query OK, 5 rows affected (0.11 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> show tables;
+----------------------+
| Tables_in_sqlstudent |
+----------------------+
| r                    |
| s                    |
| s_copy               |
| stu                  |
+----------------------+
4 rows in set (0.00 sec)

-- 其他DBMS
SELECT * INTO s_copy FROM s;
```

## 更新和删除数据

```sql
mysql> UPDATE stu
    -> SET sex="boy",
    ->     birthday=Null
    -> WHERE name = "dapeng";
Query OK, 1 row affected (0.08 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

* 可以只写一条UPDATE语句更新多列数据
* 部分DBMS支持FROM语法，把别的表中的数据更新到这张表里
* 不写WHERE语句会更新所有行
* UPDATE允许使用子查询

```sql
mysql> DELETE FROM stu WHERE id=2;
Query OK, 1 row affected (0.04 sec)
```

* 不写WHERE语句会删除所有数据
* DELETE不需要列名或通配符，应为它删除的是整个行
* 如果想删除所有行，应该使用TRUNCATE TABLE，它更快，所以无论何时，使用DELETE时记得加WHERE

## 创建和操纵表

删除表

```sql
mysql> DROP TABLE s_copy;
Query OK, 0 rows affected (0.07 sec)
```

* 没提示确认

创建表

```sql
mysql> CREATE TABLE Products(
    -> id int(255) NOT NULL,
    -> name VARCHAR(100) NULL
    -> );
Query OK, 0 rows affected (0.08 sec)
```

* 不同DBMS的表创建语句有差异
* 创建新表时，指定的表名必须不存在
* 创建表时字段允许为空则指定NULL，否则，如果要求插入时必须给出值，则指定为NOT NULL
* `NULL`不同于`''`,前者是没有值，后者是空字符串
* 不指定时大部分DBMS默认为NULL，但DB2不指定会报错
* 允许NULL值的列不允许作为主键
* DEFAULT 用来指定默认值，常用于时间或时间戳列

获取系统日期

|DBMS|函数|
|----|----|
|Access|NOW()|
|DB2|CURRENT_DATE|
|MySQL|CURRENT_TIMESTAMP|
|Oracle|SYSDATE|
|PostgreSQL|CURRENT_DATE|
|SQL Server|GETDATE()|
|SQLite|date('now')|

```sql
CREATE TABLE User
(
    id      INT(255)        NOT NULL,
    name    VARCHAR(255)    NOT NULL,
    create_time timestamp   DEFAULT CURRENT_TIMESTAMP
);
```

更新表 ALTER TABLE

* 一般不要在表中包含数据时更新表
* 所有DBMS都允许怎加列，不过对所增加列的数据类型（NULL和DEFAULT的使用）有限制
* 许多DBMS不允许删除或更改列
* 许多DBMS允许重命名列

```sql
-- 增加列
ALTER TABLE User ADD phone CHAR(20);

mysql> DESCRIBE User;
+-------------+--------------+------+-----+-------------------+-------------------+
| Field       | Type         | Null | Key | Default           | Extra             |
+-------------+--------------+------+-----+-------------------+-------------------+
| id          | int(255)     | NO   |     | NULL              |                   |
| name        | varchar(255) | NO   |     | NULL              |                   |
| create_time | timestamp    | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| phone       | char(20)     | YES  |     | NULL              |                   |
+-------------+--------------+------+-----+-------------------+-------------------+
4 rows in set (0.00 sec)
```

```sql
-- 删除列
ALTER TABLE User DROP COLUMN phone;
```
