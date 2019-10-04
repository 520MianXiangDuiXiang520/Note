package Note.Chapter8_3;

class Meal{
    private Lettuce h = new Lettuce();
    Meal(){
        System.out.println("meal");
    }
}

class Bread{
    private Lettuce h = new Lettuce();
    Bread(){
        System.out.println("bread");
    }
}

class Cheese{

    Cheese(){
        System.out.println("Cheese");
    }
}

class Lettuce{
    Lettuce(){
        System.out.println("Lettuce");
    }
}

class Lunch extends Meal{
    public void drow(){
        System.out.println("Lunch drow");
    }
    private static Lettuce h = new Lettuce();
    Lunch(){
        drow();
        System.out.println("lunch");
    }
}

class ProTableLunch extends Lunch{
    public void drow(){
        System.out.println("Pro drow");
    }
    ProTableLunch(){
        drow();
        System.out.println("protablelunch");
    }
}

public class Sandwich extends ProTableLunch {
    private static Bread bb = new Bread();
    private Bread b = new Bread();
    private Cheese c = new Cheese();
    private Lettuce l = new Lettuce();
    private int s = 1;
    public void drow(){
        System.out.println("sandwich drow" + s);
    }
    public Sandwich(){
        System.out.println("sandwich");
        drow();
    }

    public static void main(String[] args) {
        System.out.println("main");
        new Sandwich();
    }
}

//Lettuce
//Lettuce
//bread
//main
//Lettuce
//meal
//lunch
//protablelunch
//Lettuce
//bread
//Cheese
//Lettuce
//sandwich

