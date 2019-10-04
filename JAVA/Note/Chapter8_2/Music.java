package Note.Chapter8_2;

public class Music {
    public static void turn(Instrument i){
        i.play(Note.B_FLAT);
    }

    public static void main(String[] args) {
        Instrument i = new Wind();
        turn(i);
    }
}
