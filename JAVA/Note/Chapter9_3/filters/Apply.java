package Note.Chapter9_3.filters;
import static junbao.tool.Print.*;

public class Apply {
    //  策略模式
    public static void process(Processor p, Object s){
        coutln("Using Process :" + p.name());
        coutln(p.process(s));
    }
    public static void main(String[] args) {
        Waveform w = new Waveform();
        process(new FilterAdapter(new LowPass(1.0)),w);
        process(new FilterAdapter(new HighPass(1.0)),w);
    }
}
