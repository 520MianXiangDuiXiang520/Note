<!--961032830987546d0e6d54829fc886f6-->

目录(Catalo)

* [SQL操作](#SQL%E6%93%8D%E4%BD%9C)
  * [1.DML 和 DDL](#1.DML%20%E5%92%8C%20DDL)
    * [1.1 DML](#1.1%20DML)
      * [1.1.1 SELECT](#1.1.1%20SELECT)
      * [1.1.2 INSERT INTO](#1.1.2%20INSERT%20INTO)
      * [1.2.3 UPDATE](#1.2.3%20UPDATE)
      * [1.2.4 DELETE](#1.2.4%20DELETE)
    * [1.2 DDL](#1.2%20DDL)
      * [1.2.1 CREATE DATABASE](#1.2.1%20CREATE%20DATABASE)
      * [1.2.2 ALTER DATABASE](#1.2.2%20ALTER%20DATABASE)
      * [1.2.3 CREATE TABLE](#1.2.3%20CREATE%20TABLE)

<!--a46263f7a69f33f39fc26f907cdb773a-->
# SQL操作

## 1.DML 和 DDL

* DML：数据操作语言
  * SELECT：从数据库中获取数据
  * UPDATE：更新数据
  * DELETE：删除数据
  * INSERT INTO：插入数据
* DDL：数据定义语言
  * CREATE DATABASE：创建数据库
  * ALTER DATABASE：修改数据库
  * CREATE TABLE:创建数据表
  * ALTER TABLE：修改数据表
  * DROP TABLE：删除数据表
  * CREATE INDEX：创建索引
  * DROP INDEX：删除索引

### 1.1 DML

#### 1.1.1 SELECT

一般查询

```sql
SELECT 列名 FROM 表名

SELECT * FROM 表名
```

返回表中唯一不相同的值

```sql
SELECT DISTINCT 列名 FROM 表名
```

按条件查询

```sql
SELECT 列名 FROM 表名 WHERE 条件1 AND／OR 条件2

SELECT * FROM 表名 WHERE 条件1 AND/OR　条件２
```

对结果集排序：DESC降序，ASC升序

```sql
SELECT 列名 FROM 表名 ORDER BY 排序依据1 DESC，排序依据2 ASC
```

#### 1.1.2 INSERT INTO

插入行

```sql
INSERT INTO 表名 VALUES (值1，值2...)
```

插入列

```sql
INSERT INTO 表名 (列1,列2...) VALUES (值1，值2...)
```

#### 1.2.3 UPDATE

```sql
UPDATE 表名 SET 列名1=新值1,列名2=新值2 WHERE 列名=值
```

#### 1.2.4 DELETE

```sql
DELETE FROM 表名 WHERE 列名 = 值
```

### 1.2 DDL

#### 1.2.1 CREATE DATABASE

```sql
CREATE DATABASE 数据库名
```

#### 1.2.2 ALTER DATABASE

#### 1.2.3 CREATE TABLE

```sql
CREATE TABLE 表名
(
列名1 数据类型,
列名2 数据类型,
列名3 数据类型,
....
)
```

数据类型

|数据类型|描述|
|----------|----|
|integer( size )   int(size) smallint(size) tinyint(size)| 仅容纳整数。在括号内规定数字的最大位数|
|decimal(size,d) numeric(size,d)|容纳带有小数的数字。"size" 规定数字的最大位数。"d" 规定小数点右侧的最大位数|
|char(size)|容纳固定长度的字符串（可容纳字母、数字以及特殊字符）。在括号中规定字符串的长度。|
|varchar(size)|容纳可变长度的字符串（可容纳字母、数字以及特殊的字符）。在括号中规定字符串的最大长度。|
|date(yyyymmdd)|容纳日期。|

sql约束

* NOT NULL：不接受NULL值
* UNIQUE 约束唯一标识数据库表中的每条记录。
* PRIMARY KEY： 约束唯一标识数据库表中的每条记录。主键必须包含唯一的值。主键列不能包含 NULL 值。每个表都应该有一个主键，并且每个表只能有一个主键。
* FOREIGN KEY：一个表中的 FOREIGN KEY 指向另一个表中的 PRIMARY KEY。
* CHECK： 约束用于限制列中的值的范围。如果对单个列定义 CHECK 约束，那么该列只允许特定的值。如果对一个表定义 CHECK 约束，那么此约束会在特定的列中对值进行限制。
* DEFAULT: 约束用于向列中插入默认值。
