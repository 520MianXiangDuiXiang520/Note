package Note.Chapter9_3.filters;

public class LowPass extends Filter {
    double coutoff;
    public LowPass(double coutoff){
        this.coutoff = coutoff;
    }
    public Waveform process(Waveform input){
        return input;
    }
}
