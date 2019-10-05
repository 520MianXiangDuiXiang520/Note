package Note.Chapter9_3;
import static junbao.tool.Print.*;

import java.util.Arrays;

class Processor{
    public String name(){
        return getClass().getSimpleName();
    }
    Object process(Object input){
        return input;
    }
}

class Upcase extends Processor{
    String process(Object input){
        return ((String)input).toUpperCase();
    }
}

class Downcase extends Processor{
    String process(Object input){
        return ((String)input).toLowerCase();
    }
}

class Splitter extends Processor{
    String process(Object input){
        return Arrays.toString(((String)input).split(" "));
    }
}

public class Apply {
    // 策略模式
    public static void process(Processor p, Object o){
        coutln("Using processor is: " + p.name());
        coutln(p.process(o));
    }
    public static String s = "I am Iron Man";

    public static void main(String[] args) {
        process(new Upcase(), s);
        process(new Downcase(), s);
        process(new Splitter(), s);
    }
}
