package Note;

public class Money {


    public static void main(String[] args) {
        double Principal = 100;
        double interestRate = 0.0006;
        int month = 4;
        for(int i=0; i<month;i++){
            Principal += Principal * interestRate;
        }
        System.out.println(Principal);
    }
}
