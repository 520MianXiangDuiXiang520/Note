package Note.Chapter9_4;
import static junbao.tool.Print.*;

interface CanFight{
    void fight();
}

interface CanSwim{
    void swim();
}

interface CanFly{
    void fly();
}

class ActionCharacter{
    public void fight(){
        coutln("ActionCharacter fight");
    }
}

class Hreo  extends ActionCharacter implements CanFight, CanFly,CanSwim{
    public void fly(){
        coutln("Hero fly");
    }
    public void swim(){
        coutln("hero swim");
    }
}

public class Adventure {
    public static void a(CanFight c){
        c.fight();
    }
    public static void b(CanSwim s){
        s.swim();
    }
    public static void c(CanFly f){
        f.fly();
    }
    public static void d(ActionCharacter ac){
        ac.fight();
    }
    public static void main(String [] args){
        Hreo h = new Hreo();
        h.fly();
        h.swim();
        h.fight();
        a(h);
        b(h);
        c(h);
        d(h);
    }


}
