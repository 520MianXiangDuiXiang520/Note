package Note.Chapter9_3.filters;

// 波形
public class Waveform {
    private static long counter;
    private final long id = counter ++;
    public String toString(){
        return "Waveform" + id;
    }
}
