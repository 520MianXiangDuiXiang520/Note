# JSON 解析

常见的json解析器：

* jsonlib
* Gson(谷歌)
* fastjson(阿里)
* jackson(Spring内置)

## jackson

### 依赖jar包

* jackson-annotations/
* jackson-core/
* jackson-databind/

[官网下载地址](http://repo1.maven.org/maven2/com/fasterxml/jackson/core/)
		
### Java对象转JSON

#### 核心对象

`ObjectMapper`

#### 常用转换方法

* writeValue(参数1, obj)
* 参数1：
    1. File: 将obj转换为json字符串，并保存到指定文件
    2. Write: 将obj对象转换为JSON字符串，并将json数据填充到字符输出流中
    3. OutputStream: 将obj对象转换为JSON字符串，并将json数据填充到字节输出流中
* writeValueAsString(obj):  将obj对象转换为JSON字符串
* 复杂对象如List或Map转换与普通JavaBean对象一样。

#### 常用注解

* `@JsonIgnore`: 排除属性(加在类属性上)
* `@JsonFormat(pattern = "yyyy-MM-dd")`: 属性值得到格式化

### JSON转Java对象

方法：

`readValue(json字符串, obj)`

### 示例

```java
import com.fasterxml.jackson.annotation.JsonIgnore;
public class User {
    private String id;
    private String name;
    private String sex;
    private String tel;
    private String place;

    @JsonIgnore
    private String password;

    // getattr....
    // serattr....
}
```

```java
package top.junebao.test;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import top.junebao.domain.User;

import java.io.IOException;

public class JsonTest {

    private ObjectMapper objectMapper = new ObjectMapper();

    /**
     * obj对象转JSON字符串单元测试
     */
    @Test
    public void testObjToJson() {
        User user = new User();
        user.setId("LS-N4");
        user.setName("公孙胜");
        user.setPassword("gss111111");
        user.setSex("男");
        String json = "";

        try {
            json = objectMapper.writeValueAsString(user);
        } catch (JsonProcessingException e) {
            e.printStackTrace();
        }
        System.out.println(json);
    }

    /**
     * json字符串转obj单元测试
     */
    @Test
    public void testJsonToObj() {
        User user = null;
        String json = "{\"id\":\"LS-N4\",\"name\":\"公孙胜\",\"sex\":\"男\",\"tel\":null,\"place\":null}";
        try {
            user = objectMapper.readValue(json, User.class);
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println(user);
    }
}

```
