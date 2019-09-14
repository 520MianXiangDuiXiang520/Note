package Note;

class Cup {
    Cup(int marker){
        System.out.println("Cup:(" + marker + ")");
    }
    void f(int marker){
        System.out.println("f (" + marker + ")");
    }
}

class Cups{
    static Cup cup1;
    static Cup cup2;
    static{
        cup1 = new Cup(1);
        cup2 = new Cup(2);
    }
    Cups(){
        System.out.println("cups()");
    }
}

public class Chapter5_7_3 {
    public static void main(String[] args) {
        System.out.println("main()");
//        Cups.cup1.f(99);  // 使用类名调用静态属性
        cups1.cup1.f(99);
    }
    static Cups cups1 = new Cups();
}

//main()
//Cup:(1)
//Cup:(2)
//f (99)