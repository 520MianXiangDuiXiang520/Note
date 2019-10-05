package Note.Chapter9_3.filters;

public class Filter {
    public String name(){
        return getClass().getSimpleName();
    }
    public Waveform process(Waveform input){
        return input;
    }


}
