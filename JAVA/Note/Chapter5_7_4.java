package Note;

class Mug {
    Mug(int marker){
        System.out.println("Mug(" + marker + ")");
    }
    void f(int marker){
        System.out.println("f(" + marker + ")");
    }
}

public class Chapter5_7_4 {
    // 实例初始化，只要调用显式构造器，实例初始化语句就会被执行
    Mug mug1;
    Mug mug2;
    {
        mug1 = new Mug(1);
        mug2 = new Mug(2);
        System.out.println("mug1 & mug2 initialized");
    }
    Chapter5_7_4(){
        System.out.println("Chapter5_7_4()");
    }
    Chapter5_7_4(int i){
        System.out.println("Chapter5_7_4(int)");
    }

    public static void main(String[] args) {
        System.out.println("main()");
        new Chapter5_7_4();
        System.out.println("create Chapter5_7_4()");
        new Chapter5_7_4(1);
        System.out.println("create Chapter5_7_4(int)");
    }
}

//main()
//Mug(1)
//Mug(2)
//mug1 & mug2 initialized
//Chapter5_7_4()
//create Chapter5_7_4()
//Mug(1)
//Mug(2)
//mug1 & mug2 initialized
//Chapter5_7_4(int)
//create Chapter5_7_4(int)
