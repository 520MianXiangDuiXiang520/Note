package Note.Chapter8_1;

class Father{
    public void print(){
        System.out.println("Father");
    }

    public static void staticPrint(){
        System.out.println("staticFather");
    }
}

class Son extends Father{
    public void print(){
        System.out.println("Son");
    }
    public static void staticPrint(){
        System.out.println("staticSon");
    }
    public void add(){
        System.out.println("add son");
    }
}

public class Demo  {
    public static void main(String[] args) {
        Father f = new Son();
        boolean i = f instanceof Father;
        System.out.println(i);
        f.print();
        ((Son) f).add();
        f.staticPrint();
    }
}

//Son
//staticFather