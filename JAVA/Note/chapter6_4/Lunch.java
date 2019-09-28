// Note/chapter6_4/Lunch.java
package Note.chapter6_4;
import static Note.chapter6_4.Soup.*;
import static Note.chapter6_4.Soup2.*;

public class Lunch {
    public static void main(String[] args) {
        // Soup中所有构造器都被声明为private，类外无法创建实例
        // Soup s = new Soup();
        Soup soup = makeSoup();
        makeSoup();
        makeSoup();
        Soup2 Soup2 = makeSoup2();
        makeSoup2();
        makeSoup2();
    }
}
