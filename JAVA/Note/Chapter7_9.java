package Note;
import static junbao.tool.Print.*;

class Insect{
    private int i = 9;
    protected int j = 0;
    Insect(){
        coutln("Insect i = " + i + " j = " + j);
        j = 39;
    }
    private static int x1 = printInit("static x1 init");
    private int x3 = printInit("base class no static");
    static int printInit(String s){
        coutln(s);
        return 47;
    }
}

public class Chapter7_9 extends Insect{
    private int k = printInit("Chapter7_9 k init");
    public Chapter7_9(){
        coutln("k = " + k);
        coutln("j = " + j);
    }
    private static int x2 = printInit("Chapter7_9 static x2 init ");

    public static void main(String[] args) {
        coutln("main()");
        Chapter7_9 c = new Chapter7_9();
    }
}

// static x1 init
// Chapter7_9 static x2 init
// main()
// Insert i = 9 j = 39
// Chapter7_9 k init
// k = 47
// j = 39