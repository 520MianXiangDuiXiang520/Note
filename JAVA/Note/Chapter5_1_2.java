package Note;

public class Chapter5_1_2 {
    int func(int args){
        System.out.println("int func1(int args) " + args);
        return args;
    }
    float func(int args, float args2){
        System.out.println("float func(int args, float args2)" + args + args2);
        return args;
    }

    public static void main(String[] args) {
        Chapter5_1_2 c = new Chapter5_1_2();
        System.out.println(c.func(1));
        System.out.println(c.func(1,1));
        System.out.println(c.func('h'));
    }
}
