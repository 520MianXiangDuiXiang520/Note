package Note;

public class Chapter5_9 {
    public enum Spiciness{
        NOT, MILD, MEDIUM, HOT, FLAMING
    }
    Spiciness degree;

    Chapter5_9(Spiciness degree){
        this.degree = degree;
    }

    public void describe(){
        System.out.print("This burrito is ");
        switch(this.degree){
            case NOT:
                System.out.println("not spicy at all");
                break;
            case MILD:
            case MEDIUM:
                System.out.println("a little hot");
                break;
            case FLAMING:
            case HOT:
                default:
                System.out.println("maybe too hot.");
        }
    }
    public static void main(String[] args) {
        Chapter5_9
                plain = new Chapter5_9(Spiciness.NOT),
                greenChile = new Chapter5_9(Spiciness.MEDIUM),
                jalapeno = new Chapter5_9(Spiciness.HOT);
                plain.describe();
                greenChile.describe();
                jalapeno.describe();
    }
}
