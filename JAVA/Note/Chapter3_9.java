package Note;

public class Chapter3_9 {
    public static void main(String[] args) {
        // 直接常量
        int x1 = 0x2f;
        System.out.println("x1:" + x1 + " 二进制：" + Integer.toBinaryString(x1));
        int x2 = 0177;
        System.out.println("x2:" + x2 + " 二进制：" + Integer.toBinaryString(x2));
        char x3 = 0xffff;
        System.out.println("x3:" + x3 + " 二进制：" + Integer.toBinaryString(x3));
        byte x4 = 0x7f;
        System.out.println("x4:" + x4 + " 二进制：" + Integer.toBinaryString(x4));
        short x5 = 0x7fff;
        System.out.println("x5:" + x5 + " 二进制：" + Integer.toBinaryString(x5));
        long n1 = 200;
        long n2 = 200L;
        System.out.println("n1: " + n1);
        System.out.println("n2：" + n2);
    }
}