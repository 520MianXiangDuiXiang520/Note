package Note;

public class Chapter5_8 {
    public static void main(String[] args) {
        // 基本数据类型
        int [] array_int = new int [20];
        for(int i: array_int){
            System.out.print(i);
        }
        System.out.println();
        // 非基本数据类型
        Integer [] array_integer = new Integer[20];
        for(int i=0;i<array_integer.length;i++){
            array_integer[i] = new Integer(0);
        }
        for(int i: array_integer){
            System.out.print(i);
        }
        System.out.println();

        Integer [] a;
        a = new Integer[]{
                new Integer(1),
                new Integer(2),
        };

        for(Integer i: a){
            System.out.print(i);
        }

        System.out.println();
        Integer [] b = {
                new Integer(1),
                new Integer(2),
        };
        for(Integer i: b){
            System.out.print(i);
        }

    }
}
