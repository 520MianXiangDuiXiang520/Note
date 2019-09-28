package Note;
import static junbao.tool.Print.*;

class Demo {
    private String s;
    Demo(String name){
        s = name;
        coutln("new Demo object" + s);
    }
    public String toString(){
        return s;
    }
}

public class Chapter7_1 {
    // 定义时初始化
    private Demo demo = new Demo("demo");
    private Demo demo2, demo3;

    Chapter7_1(){
        // 构造器中初始化
        demo2 = new Demo("demo2");
    }

    public String toString(){
        if (demo3 == null){
            demo3 = new Demo("demo3");
        }
        return "demo3:" + demo3 + "  demo2" + demo2 + "  demo" + demo;
    }

    public static void main(String[] args) {
        Chapter7_1 c = new Chapter7_1();
        coutln(c);
    }
}
