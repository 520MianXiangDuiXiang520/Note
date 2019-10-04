package exercise;
import java.util.Arrays;
//  吸血鬼数字是指位数为偶数的数字，可以由一对数字相乘得到，而这对数字包含乘积的一半位数的数字，其中从最初的数字中选取的
//  数字可以任意排序，而两个零结尾的数字是不允许的，写一个程序，找出四位数的所有吸血鬼数字
public class exercise_10 {
    public static void main(String[] args) {
        int start, end;
        int num = 0;
        boolean istwo = false;
        int [] tar = new int[10];
        for (int i=11;i<100;i++){
            istwo = false;
            start = 1000 / i;
            end = 9999/i;
            for (int j=start;j<end;j++){
                int target=i*j;
                if (target<1000||target>9999){
                    continue;
                }

                int[] targetNum = { target / 1000, target / 100 % 10, target / 10 % 100 % 10, target%10 };
                int[] strNum = { i % 10, i / 10, j % 10, j / 10 };
                Arrays.sort(targetNum);
                Arrays.sort(strNum);
                if (Arrays.equals(targetNum,strNum) ){
                    for (int p: tar){
                       if(p == target){
                           istwo = true;
                           break;
                       }
                   }

                    if(!istwo){
                        tar[num] = target;
                        System.out.println(target + " = " + i + " * " + j);
                        num ++;
                    }

                }
            }
        }
    }
}
