package Note.Chapter9_3.filters;

class FilterAdapter implements Processor {
    Filter filter;
    FilterAdapter(Filter filter){
        this.filter = filter;
    }
    public String name(){
        return filter.name();
    }
    public Waveform process(Object s){
        return filter.process((Waveform)s);
    }
}
public class FilterProcessor{
    public static void main(String[] args) {
        Waveform w = new Waveform();
        Apply.process(new FilterAdapter(new LowPass(1.0)),w);
    }
}