package Note.Chapter9_1;
import static junbao.tool.Print.*;

abstract class Language{
    Language(){
        print();
    }
    abstract void print();
}

class Chinese extends Language{
    private int sum = 9;
    public void print(){
        coutln(sum);
    }
}

public class Exercise2 {
    public static void main(String[] args) {
        Chinese c = new Chinese();
//        Language c = new Chinese();
        c.print();
    }
}
