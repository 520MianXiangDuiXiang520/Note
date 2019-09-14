package Note;

public class Chapter5_1 {
    // 在构造器中使用构造器
    int num = 0;
    String str = "";

    Chapter5_1(){
//        System.out.println("hello");  // 在构造器中使用构造器，this必须作为第一条语句
        this(5);
//        this(5,"hell0");  // 一个构造器内只能调用一个构造器
        System.out.println("没有参数的构造器");
    }
    Chapter5_1(int n){
        this(n,"hello");
        num = n;
        System.out.println("有一个int参数的构造器");
    }
    Chapter5_1(int n,String s){
        str = s;
        System.out.println("有两个参数的构造器");
    }
    void print(){
        System.out.println("num = " + num + ", str = " + str);
    }

    public static void main(String[] args) {
        Chapter5_1 obj = new Chapter5_1();
        obj.print();
    }
}
//    有两个参数的构造器
//    有一个int参数的构造器
//    没有参数的构造器
//    num = 5, str = hello
