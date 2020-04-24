# MySQL 总结

## 什么是MySQL

一种关系型数据库，遵循GPL开源许可， 默认端口3306

## 存储引擎

查看MySQL 提供的所有存储引擎：

```sql
show engines;
```

* 默认`InnoDB`

### MyISAM 和 InnoDB 的区别

* MySQL 5.5之前默认使用 MyISAM, 5.5 之后默认是 InnoDB
* MyISAM 只支持表级锁， InnoDB 支持行级锁和表级锁（默认行级锁）
* InnoDB 支持事务和崩溃后的恢复
* InnoDB 支持外键
* InnoDB 支持[MVCC](https://blog.csdn.net/Waves___/article/details/105295060)

## 索引

## 事务隔离级别





## 其他

1. 数据库找到最新插入的那个记录
2. 