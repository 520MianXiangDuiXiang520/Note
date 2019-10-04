package exercise.exercise8_5;
import static junbao.tool.Print.*;

class StarShip{
    public void ship(){}
}

class DangerStarShip extends StarShip{
    public void ship(){
        coutln("DANGER StarShip");
    }
}

class NervousStarShip extends StarShip{
    public void ship(){
        coutln("NERVOUS StarShip");
    }
}

class PeaceStarShip extends StarShip{
    public void ship(){
        coutln("PEACE StarShip");
    }
}

class Space{
    private StarShip alertStatus = new PeaceStarShip();
    private int danger_level = -1;
    private void changeDanger(){
        if(danger_level  == 0){
            alertStatus = new NervousStarShip();
        }
        else if (danger_level < 0){
            alertStatus = new PeaceStarShip();
        }
        else {
            alertStatus = new DangerStarShip();
        }
    }
    public void addDanger(){
        danger_level ++;
        changeDanger();
    }
    public void subtractDanger(){
        danger_level --;
        changeDanger();
    }
    public void fly(){
        alertStatus.ship();
    }

}

public class Transmogrify {
    public static void main(String[] args) {
        Space s = new Space();
        s.fly();
        s.addDanger();
        s.fly();
        s.addDanger();
        s.fly();
        s.subtractDanger();
        s.fly();
    }
}
