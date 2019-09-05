import java.util.Scanner;
public class Squire {
    public static void main(String [] args){
        System.out.println("please input the size:");
        Scanner input = new Scanner(System.in);
        int size = input.nextInt();
        int [][] sq = new int[size][size];
        int p;
        if(size % 2 != 0){
            p = size + 1;
        }else{
            p = size;
        }
        for(int i=0;i<p/2;i++){
            int num = 0;
            for(int j=0;j<p/2;j++){
                if(i>=j){
                    num ++;
                }
                sq[i][j] = num;
                sq[size-i-1][j] = num;
                sq[i][size-j-1] = num;
                sq[size-i-1][size-j-1] = num;
            }
        }
        for(int i=0;i<size;i++){
            for(int j=0;j<size;j++){
                System.out.print(sq[i][j] + " ");
            }
            System.out.println();
        }
    }
}
