package exercise;
// 创建一个enum，包含纸币中最小面值的六种类型，通过values()循环并打印每一个值及其ordinal()
public class exercise_21 {
    public enum Money{
        ONE, TEN, HUNDRED, THOUSANDS, MILLION, BILLION
    }

    public static void main(String[] args) {
        for(Money i: Money.values()){
            System.out.println(i + "(" + i.ordinal() + ")");
        }
    }
}
