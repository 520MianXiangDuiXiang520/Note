public class Feibe {

    private static void FeiBe(int first,int second, int n, int i){
        int third;
        third = first + second;
        first = second;
        second = third;
        i ++;
        if(third > 0 && i < n){
            System.out.print(third + " ");
            FeiBe(first, second, n, i);
        }
        else if (third < 0){
            System.out.println("第" + (i+2) +"项溢出");
        }
    }
    public static void main(String[] args){
        int n = 100;
        int first = 1;
        int second = 1;
        int i = 0;
        FeiBe(first, second, n, i);
    }
}
