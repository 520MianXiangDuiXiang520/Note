package Note;
import static junbao.tool.Print.*;

class Proxy{
    protected void run(String s){
        coutln("run()");
    }
    protected void jump(){
        coutln("jump()");
    }
}

public class Chapter7_5 {
    private Proxy proxy;
    Chapter7_5(){
        proxy = new Proxy();
    }
    public void run(String s){
        proxy.run(s);
    }
    public void jump(){
        proxy.jump();
    }
}
