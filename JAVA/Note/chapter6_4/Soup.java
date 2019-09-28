// Note/chapter6_4/Soup.java
package Note.chapter6_4;
import static junbao.tool.Print.*;

class Soup {
    private static int nums = 0;
    private Soup(){
        this.nums ++;
        coutln("beautiful soup :  " + this.nums);
    }
    public static Soup makeSoup(){
        return new Soup();
    }
}

class Soup2{
    private int nums = 0;
    private Soup2(){
        this.nums ++;
        coutln("beautiful soup2 : " + this.nums);
    }
    // 单例模式
    private static Soup2 soup2 = new Soup2();
    public static Soup2 makeSoup2(){
        return soup2;
    }
}
