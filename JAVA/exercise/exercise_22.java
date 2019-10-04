package exercise;
import exercise.exercise_21;
// 在前面的例子中，为enum写一个switch语句，对于每一个case，输出特定的描述
public class exercise_22 {
    exercise_21.Money money;
    exercise_22(exercise_21.Money money){
        this.money = money;
    }
    public void Description(){
        switch(this.money){
            case ONE:
                System.out.println("一元");
                break;
            case TEN:
                System.out.println("十元");
                break;
            case HUNDRED:
                System.out.println("百元");
                break;
            case THOUSANDS:
                System.out.println("千元");
                break;
            case MILLION:
                System.out.println("万元");
                break;
            case BILLION:
                default:
                System.out.println("亿元");
        }
    }

    public static void main(String[] args) {
        exercise_22 m1, m2, m3;
        {
            m1 = new exercise_22(exercise_21.Money.ONE);
            m2 = new exercise_22(exercise_21.Money.TEN);
            m3 = new exercise_22(exercise_21.Money.BILLION);
        }
        m1.Description();
        m2.Description();
        m3.Description();
    }
}
