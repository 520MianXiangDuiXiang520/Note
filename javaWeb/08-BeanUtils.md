# BeanUtils的使用

用于快速分装JavaBean对象  

[jar包](http://commons.apache.org/proper/commons-beanutils/download_beanutils.cgi)

## 常用方法

1. `setProperty()`: 设置属性
2. `getProperty()`: 获取属性
3. `populate()`: 根据Map分装对象

```java
Map<String, String[]> parameterMap = req.getParameterMap();
        User loginUser = new User();
        try {
            BeanUtils.populate(loginUser, parameterMap);
            System.out.println(BeanUtils.getProperty(loginUser, "name"));
            BeanUtils.setProperty(loginUser, "name", "lisi");
        } catch (IllegalAccessException | InvocationTargetException e) {
            e.printStackTrace();
        }
```