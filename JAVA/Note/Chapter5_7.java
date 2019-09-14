package Note;

/**
 * 在类的内部，变量定义的先后顺序取决于初始化的顺序，即使变量定义散布于方法定义间，他们仍会在任何方法之前得到初始化
 */

class Window {
    Window(int no){
        System.out.println("Chapter5_7:" + no + ";");
    }
}
class House{
    House(){
        System.out.println("Chapter5_7构造器");
        Window d1 = new Window(1);
    }
    Window d2 = new Window(2);
    void c1(){
        System.out.println("c1()");
    }
    Window d3 = new Window(3);
}
public class Chapter5_7 {
    public static void main(String[] args) {
        House house = new House();
        house.c1();
    }
}
//Chapter5_7:2;
//Chapter5_7:3;
//Chapter5_7构造器
//Chapter5_7:1;
//c1()
