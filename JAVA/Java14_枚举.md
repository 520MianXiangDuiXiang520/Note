# 枚举

类比单例模式，是一个特殊的类，可以实现接口。但不能继承，不能用new实例化，内部提供有限数量的实例：

```java
package Note.enumDemo;

interface Poem {
    void poem();
}

// 枚举类型可以实现接口，如果覆写的方法直接跟在内部实例后面那每个实例都可以表现出不同的行为，
// 也可以定义在下面，让多个实例公用一个方法
public enum Season implements Poem{
    // 定义实例，必须放在最初，是public static final的
    SPRING("春天") {
        @Override
        public void poem() {
            System.out.println("春眠不觉晓");
        }
    },
    SUMMER("夏天") {
        @Override
        public void poem() {
            System.out.println("连雨不知春去，一晴方觉夏深");
        }
    },
    AUTUMN("秋天") {
        @Override
        public void poem() {
            System.out.println("自古逢秋悲寂寥");
        }
    },
    WINTER("冬天") {
        @Override
        public void poem() {
            System.out.println("忽如一夜春风来");
        }
    };

    private String hans;
    private Season(String hans) {
        this.hans = hans;
    }
    
    @Override
    public String toString() {
        return "Season{" +
                "hans='" + hans + '\'' +
                '}';
    }
}

```

```java
package Note.enumDemo;

public class Main {
    public static void main(String[] args) {
        // 获取实例名
        String name = Season.SUMMER.name();
        System.out.println(name);

        // 获取所有实例的数组
        Season[] values = Season.values();
        for (int i = 0; i < values.length; i++) {
            System.out.println(values[i].toString());
        }
        
        // 调用实例的方法
        Season.SUMMER.poem();

        // 通过实例名获取实例
        Season spring = Season.valueOf("SPRING");
        System.out.println(spring);
    }
}
```

