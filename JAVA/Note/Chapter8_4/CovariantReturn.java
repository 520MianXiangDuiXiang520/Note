package Note.Chapter8_4;
import static junbao.tool.Print.*;

// 协变返回类型
class Grain{
    public String toString(){
        return "Grain";
    }
}

class Wheat extends Grain{
    public String toString(){
        return "Wheat";
    }
}

class Mill{
    Grain process(){
        return new Grain();
    }
}

class WheatMill extends Mill{
    Wheat process(){
        return new Wheat();
    }
}

public class CovariantReturn {
    public static void main(String[] args) {
        Mill m = new Mill();
        Grain g = m.process();
        coutln(g);

        // 向上转型
        m = new WheatMill();
        // 向上转型
        g = m.process();
        coutln(g);
    }
}
