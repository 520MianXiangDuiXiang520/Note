package Note.Chapter9_3.exercise11;
import Note.Chapter9_3.filters.*;
class Canter implements Processor{
    StrClass s;
    Canter(StrClass s){
        this.s = s;
    }
    public String name(){
        return s.name();
    }
    public Object process(Object input){
        return s.process((String) input);
    }
}

public class StrClass {
    public String name(){
        return getClass().getSimpleName();
    }
    public String process(String arg){
        return arg + "rep";
    }

    public static void main(String[] args) {
        Apply.process(new Canter(new StrClass()),"aaa");
    }
}
