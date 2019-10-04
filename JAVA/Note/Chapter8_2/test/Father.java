package Note.Chapter8_2.test;
import static junbao.tool.Print.*;

public class Father {
    public void play(){
        coutln("father play()");
    }
    public void getClassName(){
        coutln("class name is: " + getClass());
    }
    final public void finalMethod(){
        coutln("【final】class name is: " + getClass());
    }
    public static void staticMethod(){
        coutln("father static method");
    }
    private void privateMethod(){
        coutln("privateMethod in Father");
    }

    public static void main(String[] args) {
        Father f = new Son();
        f.finalMethod();  // 【final】class name is: class Note.Chapter8_2.test.Son
        f.privateMethod();  // privateMethod in Father
    }
}
