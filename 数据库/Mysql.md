# Mysql

创建数据库

```sql
CREATE DATABASE DEMO;
```

查看所有数据库

```sql
SHOW DATABASES;
```

删除数据库

```sql
DROP DATABASE demo;
```

选择数据库

```sql
use demo;
```

建立数据表

```sql
CREATE TABLE table_name(字段名, 字段属性);
```

展示表结构

```sql
DESCRIBE table_name;
```

展示所有数据表

```sql
show tables;
```

删除数据表

```sql
DROP TABLE table_name;
```

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

插入数据

```sql
-- 插入完整一行，必须保证顺序与表定义顺序相同
INSERT INTO table_name VALUES(字段值1, 字段值2，···)

-- 自定义插入，推荐
INSERT INTO table_name(字段名1,
                       字段名2,
                       ···)
VALUES(字段值1,
       字段值2,
       ···);

-- 插入检索出的数据
INSERT INTO table_name (字段名,) SELECT (字段名) FROM table_name;
```
