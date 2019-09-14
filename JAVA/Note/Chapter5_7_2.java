package Note;

class Bowl{
    Bowl(int marker){
        System.out.println("Bowl (" + marker + ")");
    }
    void f1(int marker){
        System.out.println("f1(" + marker + ")");
    }
}

class Table{
    static Bowl bowl1 = new Bowl(1);
    Table(){
        System.out.println("Table()");
        bowl2.f1(1);
    }
    void f2(int marker){
        System.out.println("f2(" + marker + ")");
    }
    static Bowl bowl2 = new Bowl(1);
}

class Cupboard{
    Bowl bowl3 = new Bowl(3);
    static Bowl bowl4 = new Bowl(4);
    Cupboard(){
        System.out.println("Cupuoard()");
        bowl4.f1(2);
    }
    void f3(int marker){
        System.out.println("f3(" + marker + ")");
    }
    static Bowl bowl5 = new Bowl(5);
}

public class Chapter5_7_2 {
    public static void main(String[] args) {
        System.out.println("Creating new Cupboard() in main");
        new Cupboard();
        System.out.println("Creating new Cupboard() in main");
        new Cupboard();
        table.f2(1);
        cupboard.f3(1);
    }

    // 变量定义会先于方法执行，所以这一句是第一个被执行的
    static Table table = new Table();
    static Cupboard cupboard = new Cupboard();
}
//Bowl (1)
//Bowl (1)
//Table()
//f1(1)
//Bowl (4)
//Bowl (5)
//Bowl (3)
//Cupuoard()
//f1(2)
//Creating new Cupboard() in main
//Bowl (3)
//Cupuoard()
//f1(2)
//Creating new Cupboard() in main
//Bowl (3)
//Cupuoard()
//f1(2)
//f2(1)
//f3(1)