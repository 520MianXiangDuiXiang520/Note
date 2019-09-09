import java.net.SocketOption;

public class Factorial {

    static public int [] Multiply(int [] first, int second){
        int [] result = new int [100000];
        int num = first.length;
        int jin = 0;
        int r;
        int j = 0;
        for(int i=num-1;i>=0;i--){
            r = ((first[i] * second) + jin) % 10;
            jin = ((first[i] * second) + jin) / 10;
            result[j] = r;
            j++;
        }
        while(jin > 10){
            r = jin % 10;
            jin = jin /10;
            result[j] = r;
            j++;
        }
        result[j] = jin;
        int [] ret = new int[j+1];
        int k = 0;
        for(int i=j;i>=0;i--){
            ret[k++] = result[i];
        }
        return ret;
    }
    static public void main(String [] args){
        int [] first = {1};
        int second = 6000;
        for(int i=1;i<=second;i++){
            first = Multiply(first, i);
        }
        for(int k: first){
            System.out.print(k);
        }
        System.out.println();
    }
}
