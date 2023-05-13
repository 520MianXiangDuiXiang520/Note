# MongoDB 入门

## 安装

[下载链接](https://www.mongodb.com/try/download/community)

## 基本概念

1. DB: 类似于 MySQL 中的一个数据库，每个 MongoDB 实例可以建立多个 DB
2. Collection: 类似于表
3. Document

## 增删查改

切换数据库：

```mongodb
use test
```

* 当数据库不存在时， 使用 use 会创建 db

查看所有数据库：

```mongodb
show dbs
```

删除当前数据库：

```mongodb
db.dropDatabase()
```

创建集合：

```mongodb
db.createCollection("testCollection", {capped: true, autoIndexId: true, size: 6142800, max: 10000}) 
```

* `createCollection(name, option)` 接收两个参数，前者表示要创建的集合名，后者是一个可选选项，可以传以下值：
  1. `capped`: 布尔值，如果为 true, 表示创建固定大小的集合，集合达到固定大小后，后面的文档会覆盖旧文档，该值为 true 时，必须指定 size
  2. `autoIndexId`: 已弃用，为 true 表示自动在 _id 字段创建索引
  3. `size`: 固定集合能占用的最大空间，单位字节
  4. `max`: 集合中能包含的最多文档数 

查看数据库下所有集合：

```mongodb
db.getCollectionNames();
```

删除某个集合

```mongodb
db.collectionName.drop()
```

插入文档

```mongodb
db.collectionName.insert(document)
```

插入多条文档

```mongodb
db.collectionName.insertMany([document1, document2, ...])
```

