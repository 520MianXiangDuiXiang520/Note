# JDBC入门

## 步骤

1. 导入驱动jar包
  * IDEA中将jar包复制到项目目录后要右击点击`add as Library`
2. 注册驱动
3. 获取数据库连接对象
4. 获取执行SQL对象
5. 执行SQL
6. 释放资源


```java
public static void main(String[] args) throws ClassNotFoundException, SQLException {
        // 注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        // 获取数据库连接对象
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/studentsgradems?serverTimezone=GMT%2B8&useUnicode=true&characterEncoding=utf-8",
                "root", "1234567");
        String sql = "INSERT INTO student VALUE('2','2', '2', '2','2','2','2','2')";
        // 获取执行SQL的对象
        Statement statement = conn.createStatement();
        boolean execute = statement.execute(sql);
        System.out.println(execute);
        // 释放资源
        statement.close();
        conn.close();
    }
```

## 对象详解

* `DriverManager`驱动管理对象
* `Connection`:数据库连接对象
* `Statement`：执行SQL的对象
* `ResultSet`：结果集对象
* `PreparedStatement`：执行SQL的对象，`Statement`的导出

### DriverManager

功能：注册驱动（registerDriver），获取数据库连接（getConnection）

代码中通过加载`com.mysql.cj.jdbc.Driver`类来注册驱动，实质上`Driver`类是将`DriverManager.registerDriver()`方法的执行放在静态代码块中，在类加载时自动执行。

```java
public class Driver extends NonRegisteringDriver implements java.sql.Driver {
    public Driver() throws SQLException {
    }

    static {
        try {
            DriverManager.registerDriver(new Driver());
        } catch (SQLException var1) {
            throw new RuntimeException("Can't register driver!");
        }
    }
}
```

MySQL5之后可以不用注册驱动。

获取数据库连接：

```java
Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/studentsgradems?serverTimezone=GMT%2B8&useUnicode=true&characterEncoding=utf-8",
                "root", "1234567");
```

参数： url(mysql):jdbc:mysql://IP:端口/数据库名
  * 本地连接可以省略IP和端口`jdbc:mysql:///dbname`

### Connection 数据库连接对象

* 功能：
  1. 获取执行SQL的对象
    * `Statement createStatement()`
    * `PreparedStatement prepareStatement(String sql)`
  2. 管理事务（要么全做，要么不做）
    * 开启事务：`void setAutoCommit(boolean autoCommit)`设置参数为false，即开启事务
    * 提交事务：`commit()`
    * 回滚事务：`rollback()`

### Statement

功能：

1. 执行SQL
  * `boolean execute()`
  * `int executeUpdate(String sql)`:执行DML， DDL语句，返回影响的行数
  * `Result executeQuery(String sql)`:执行select语句 

### ResultSet：结果集对象，分装查询结果

* next(): 游标向下移动一行，判断当前行是否是最后一行，如果是，返回false
* getInt()/getString..:获取数据
  * `int i`：第`i`列（从1开始）
  * `String name`: 根据列名

```java
String sql = "SELECT * FROM student";
// 获取执行SQL的对象
Statement statement = conn.createStatement();
ResultSet resultSet = statement.executeQuery(sql);
while(resultSet.next()) {
    String id = resultSet.getString(1);
    String sName = resultSet.getString("Sname");
    System.out.println(id + "--" + sName);
}
```

### preparedStatement 动态SQL

使用`statement`有`SQL注入`风险， 并且效率不高，一般使用`preparedStatement`,`preparedStatement`使用`?`作为占位符，然后给`?`赋值

```java
String sql = "SELECT * FROM student WHERE id = ? AND password = ?";
preparedStatement = connection.prepareStatement(sql);
preparedStatement.setString(1, id);
preparedStatement.setString(2, password);
resultSet = preparedStatement.executeQuery();
```

* 获取SQL操作对象时要传递SQL字符串（`statement`不需要）
* 使用`preparedStatement.setXxxx(int index, Xxxx value)`给`?`赋值，第一个整型参数是`?`的位置（从1开始），第二个参数是`?`值,具体类型与数据库字段类型对应。
* 执行SQL时不需要再次传递SQL字符串了

## JDBC控制事务

```java
 private void Demo(String id, String password) {
        Connection connection = null;
        String sql = "UPDATE Table SET money = money - ? WHERE userid = ?";
        String sql2 = "UPDATE Table SET money = money + ? WHERE userid = ?";
        PreparedStatement preparedStatement = null;
        PreparedStatement preparedStatement2 = null;
        try {
            connection = JDBCUtils.getConnection();
            assert connection != null;
            // 开启事务
            connection.setAutoCommit(false);
            preparedStatement = connection.prepareStatement(sql);
            preparedStatement2 = connection.prepareStatement(sql2);
            preparedStatement.setInt(1, 500);
            preparedStatement.setString(2, "wc110");
            preparedStatement2.setInt(1, 500);
            preparedStatement2.setString(2, "wc111");
            preparedStatement.executeUpdate();
            // 正常执行，提交事务
            connection.commit();
        } catch (Exception e) {
            // 不管发送什么异常，回滚事务
            connection.rollback();
            e.printStackTrace();
        } finally {
            JDBCUtils.close(connection, preparedStatement, resultSet);
        }
    }

```

## 一个JDBC工具类

```java
package top.junebao.utils;

import java.io.FileReader;
import java.io.IOException;
import java.net.URL;
import java.sql.*;
import java.util.Properties;

public class JDBCUtils {
    private static String dbUrl;
    private static String dbUser;
    private static String dbPassword;
    private static String dbDriver;

    static{
        Properties properties = new Properties();
        ClassLoader classLoader = JDBCUtils.class.getClassLoader();
        URL url = classLoader.getResource("jdbc.properties");
        assert url != null;
        String path = url.getPath();
        try {
            properties.load(new FileReader(path));
        } catch (IOException e) {
            e.printStackTrace();
        }
        dbUrl = properties.getProperty("dbUrl");
        dbUser = properties.getProperty("dbUser");
        dbPassword = properties.getProperty("dbPassword");
        dbDriver = properties.getProperty("dbDriver");
    }

    /**
     * 获取数据库连接对象
     * @return Connection
     */
    public static Connection getConnection() throws ClassNotFoundException, SQLException {
        Connection connection = null;
        Class.forName(dbDriver);
        connection = DriverManager.getConnection(dbUrl, dbUser, dbPassword);
        return connection;
    }

    /**
     * 释放数据库资源
     * @param connection 数据库连接对象
     * @param statement SQL执行对象
     */
    public static void close(Connection connection, Statement statement) {
        if(statement != null) {
            try {
                statement.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }

        if(connection != null) {
            try {
                connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * 释放数据库资源
     * @param connection 数据库连接对象
     * @param statement SQl执行对象
     * @param resultSet 查询结果集
     */
    public static void close(Connection connection, Statement statement, ResultSet resultSet) {
        close(connection, statement);
        if(connection != null) {
            try {
                connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}

```

jdbc.properties

```properties
dbUrl=jdbc:mysql:///studentsgradems?serverTimezone=GMT%2B8&useUnicode=true&characterEncoding=utf-8
dbUser=root
dbPassword=1234567
dbDriver=com.mysql.cj.jdbc.Driver
```