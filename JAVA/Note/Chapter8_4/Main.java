package Note.Chapter8_4;

class Father{
    public void a(){}
}

class Son extends Father{
    public void a(){}
    public void b(){}
}

public class Main{
    public static void main(String[] args) {
        Father [] f = {
                new Father(),
                new Son()
        };
        f[0].a();
        f[1].a();
//        f[0].b();
//        f[1].b();
//        ((Son)f[0]).b();  // Exception in thread "main" java.lang.ClassCastException:
        ((Son)f[1]).b();
    }
}