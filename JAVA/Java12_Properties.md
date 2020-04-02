```java
package Note.iosystem;

import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.util.Properties;
import java.util.Set;

public class PropertyDemo {
    public static void main(String[] args) throws IOException {
        String filePath = "./src/Note/iosystem/properties.properties";
        Properties properties = new Properties();
        // 添加值（键值都是字符串）
        properties.setProperty("name", "zhangsan");
        properties.setProperty("age", "19");
        // 序列化到磁盘（字符，字节流都可以），第二个字符串参数是注释
        properties.store(new FileOutputStream(filePath), "我是注释");
        // 从磁盘加载到容器
        properties.load(new FileReader(filePath));
        // 获得所有key的集合
        Set<String> result = properties.stringPropertyNames();
        for (String res: result
             ) {
            // 通过key获取值
            System.out.println(properties.getProperty(res));
        }
    }
}

```

HashMap实现