package Note.Chapter9_3.filters;

public class BandPass extends Filter {
    double lowcouoff, highcutoff;
    public BandPass(double lowcouoff, double highcutoff){
        this.highcutoff = highcutoff;
        this.lowcouoff = lowcouoff;
    }
    public Waveform process(Waveform input){
        return input;
    }
}
