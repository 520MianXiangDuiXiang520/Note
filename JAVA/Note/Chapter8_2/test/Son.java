package Note.Chapter8_2.test;
import static junbao.tool.Print.*;

public class Son extends Father {
    // 导出类覆盖基类方法
    public void play(){
        coutln("导出类覆盖基类方法 Son play()");
    }
    public static void staticMethod(){
        coutln("son static method");
    }
    public void privateMethod(){
        coutln("privateMethod in Son");
    }

    public static void main(String[] args) {
        Father test = new Son();
        test.play();
        // 不覆盖基类方法，调用
        test.getClassName();
        // 调用final方法
        test.finalMethod();
        // 调用static方法
        test.staticMethod();
    }
}
