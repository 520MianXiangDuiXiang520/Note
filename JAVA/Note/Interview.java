package Note;
import static junbao.tool.Print.*;

class test{
    static int num = 0;
}

public class Interview {
    static int num = 0;

    public static void main(String[] args) {
        coutln("MyTest.num=" + test.num);  // MyTest.num=0
        Interview a1 = new Interview();
        a1.num ++;
        Interview a2 = new Interview();
        a2.num ++;
        num ++;
        a1 = new Interview();
        a1.num --;
        coutln(a1.num);  // 2
    }
}
