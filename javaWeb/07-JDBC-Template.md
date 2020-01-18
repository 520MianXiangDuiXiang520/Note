# JDBC-Template

Spring 框架提供了一个 JdbcTemplate 对象，来简化JDBC的开发。

使用步骤：

1. 导入jar包

    > 需要5个依赖

    * `spring-beans-5.2.2.RELEASE.jar`
    * `spring-core-5.2.2.RELEASE.jar`
    * `spring-jdbc-5.2.2.RELEASE.jar`
    * `spring-tx-5.2.2.RELEASE.jar`
    * `com.springsource.org.apache.commons.logging-1.1.1.jar`

    * 前四个可以直接从Spring的依赖中找到，[Spring所有版本下载（官网）](https://repo.spring.io/release/org/springframework/spring/)  

    * 最后一个的[下载地址](https://mvnrepository.com/artifact/org.apache.commons/com.springsource.org.apache.commons.logging/1.1.1)

2. 创建JdbcTemplate对象，需要传入一个DataSource
3. 调用JdbcTemplate的方法完成CRUD操作
  * `update()`: 执行DML语句 增删改
  * `queryForMap()`: 将查询结果封装为Map集合,结果集长度只能是1，列名作为key，值作为value
  * `queryForList()`: 将查询结果封装为List集合，将每一条记录封装为Map，再将多个map装到List
  * `queryForObject()`: 将查询结果封装为对象,一般用于聚合函数
  * `query()`: 将查询结果封装为JavaBean对象
    * 第二个参数需要传递一个`RowMapper`对象
    * 一般使用`BeanPropertyRowMapper`实现类， 它可以完成数据到JavaBean的自动封装： `new BeanPropertyRowMapper<类>(类.class)`