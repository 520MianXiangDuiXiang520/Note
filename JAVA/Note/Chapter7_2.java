package Note;
import static junbao.tool.Print.*;

class Father{
    private String name;

    Father(String name){
        this.name = name;
    }

    public void func1(){
        coutln("func1()");
    }

    public void func1(int s){
        coutln("func1(int)");
    }

    protected void func2(Father f){
        coutln("向上转型");
    }
}

public class Chapter7_2 extends Father {
    Chapter7_2(){
        super("son");
    }
    // 如果想覆盖，但不小心写成了重载，使用@Override注解就会报错
    @Override
    public void func1(){
        coutln("覆盖func1()");
    }
    public void func(){
        super.func1();
        func2(new Chapter7_2());
    }

    public static void main(String[] args) {
        Chapter7_2 c = new Chapter7_2();
        c.func1();
        c.func1(2);
        c.func();
    }
}

//覆盖func1()
//func1(int)
//func1()
//向上转型
