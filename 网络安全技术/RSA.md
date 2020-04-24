Cowards are afraid of happiness, get hurt when they encounter cotton, and sometimes be hurt by happiness.

<!-- more -->

# RSA

* 非对称加密（相当于把锁（公钥）发给别人，钥匙（私钥）自己留着，别人拿到锁后用锁加密数据，传送给自己，自己就可以用钥匙解密了。）

## 加解密过程

1. 取两个大素数 $$p_1$$, $$p_2$$
   $$
   N = P_1 * P_2
   $$

2. 根据欧拉函数
   $$
   \varphi(N) = (p_1 - 1) * (p_2 - 1)
   $$
   计算出$$\varphi(N)$$

3. 根据欧拉定理
   $$
   d = \frac{(k * \varphi(N) + 1)}{e}
   $$

   * 其中e是一个常数，满足：$$1 < e < \varphi(N)$$且$$e与\varphi(N)互质$$
   * k也是一个常数，用来保证d是一个整数
   
4. 公钥为$$(e, N)$$

5. 私钥为$$(d, N)$$

6. 加密时有明文m,则密文c：
   $$
   m^e \ mod \  N \equiv c
   $$

7. 解密时有密文c，则明文m:
   $$
   c^d \ mod \  N = m
   $$
   

   

## 大质数的产生

这两个大质数的长度直接影响RSA算法的安全性，大质数产生分为两个步骤：

1. 伪质数的生成
2. miller_rabin 素性检测

[参考](https://blog.csdn.net/qq_35116353/article/details/71076180)

[miller_rabin代码](https://blog.csdn.net/qq_41021816/article/details/80055961)

```java
package top.junebao;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Random;

public class GetBigPrime {

    private static Integer[] getPrimeTable(int end) {
        Integer [] result = {0};
        ArrayList<Integer> list = new ArrayList<Integer>();
        for (int i = 3; i < end; i += 2) {
            list.add(i);
        }
        for (int i = 0; i < list.size(); i++) {
            for (int j = i + 1; j < list.size(); j++) {
                if(list.get(j) % list.get(i) == 0){
                    list.remove(j);
                }
            }
        }


        return list.toArray(result);
    }

    /**
     * 获取一个随机的大奇数
     * @param len 奇数的长度
     * @return 一个大奇数
     */
    private static BigInteger getBigOdd(int len) {
        StringBuilder sb = new StringBuilder();
        int [] odds = {1, 3, 7, 9};
        Random random = new Random();
        sb.append(random.nextInt(9) + 1);
        for (int i = 1; i < len - 1; i++) {
            sb.append(random.nextInt(10));
        }
        sb.append(odds[random.nextInt(3)]);
        return new BigInteger(sb.toString());
    }

    /**
     * 通过大奇数获得一个伪素数
     * @return 返回一个伪素数
     */
    private static BigInteger getPseudoPrime(int len) {
        Integer [] primeTable = null;
        if(len > 4)
            primeTable = getPrimeTable(2000);
        else if(len == 3) primeTable = getPrimeTable(200);
        else primeTable = getPrimeTable(20);
        while(true) {
            BigInteger odd = getBigOdd(len);
            int flag = 0;
            for (Integer integer : primeTable) {
                flag ++;
                if (odd.mod(new BigInteger(integer.toString())).equals(BigInteger.ZERO)) {
                    break;
                }
            }
            if(flag == primeTable.length)
                return odd;
        }
    }

    /**
     * miller_rabin 素性检测
     * https://blog.csdn.net/qq_41021816/article/details/80055961
     * @param pseudoPrime 伪素数
     * @return 如果伪素数是素数，返回true, 否则返回false
     */
    private static boolean primalityTest(BigInteger pseudoPrime) {
        if (pseudoPrime.equals(BigInteger.valueOf(0)) || pseudoPrime.equals(BigInteger.valueOf(1)))
            return false;
        if (pseudoPrime.equals(BigInteger.valueOf(2)))
            return true;
        int s=10;
        BigInteger k=pseudoPrime.subtract(BigInteger.valueOf(1));
        int t=0;
        while (k.getLowestSetBit()!=0){
            t++;
            k=k.divide(BigInteger.valueOf(2));
        }
        Random ran = new Random();
        while (s-->0){
            BigInteger a=new BigInteger(100,ran).mod(
                    pseudoPrime.subtract(BigInteger.valueOf(2))).add(BigInteger.valueOf(2) );
            BigInteger[] x= new BigInteger[105];
            x[0]=a.modPow(k,pseudoPrime);
            for (int i=1;i<=t;i++){
                x[i]=x[i-1].modPow(BigInteger.valueOf(2),pseudoPrime);
                if (x[i].equals(BigInteger.valueOf(1)) && !x[i - 1].equals(BigInteger.valueOf(1)) &&
                        !x[i - 1].equals(pseudoPrime.subtract(BigInteger.valueOf(1))))
                    return false;
            }
            if (!x[t].equals(BigInteger.valueOf(1)))
                return false;
        }
        return true;
    }

    /**
     * 获取一个素数（基于概率）
     * @param len 素数长度
     * @return 返回一个BigInteger类型的素数
     */
    public static BigInteger getBigPrime(int len) {
        BigInteger pseudoPrime = getPseudoPrime(len);
        while(!primalityTest(pseudoPrime)){
            pseudoPrime = getPseudoPrime(len);
        }
        return pseudoPrime;
    }

    public static void main(String[] args) {
        System.out.println(getBigPrime(1));
    }

}

```

## 完整代码

RSA算法

```java
package top.junebao;

import java.math.BigInteger;
import java.util.LinkedList;
import java.util.List;

public class RSA {
    private static final BigInteger E = new BigInteger("3");
    private static BigInteger N = null;
    private static BigInteger D = null;
//    private static BigInteger p1 = new BigInteger("53");
//    private static BigInteger p2 = new BigInteger("59");

    private static BigInteger p1 = null;
    private static BigInteger p2 = null;

    private static BigInteger getP1(int len) {
        if(p1 == null)
            p1 = GetBigPrime.getBigPrime(len);
        return p1;
    }

    private static BigInteger getP2(int len) {
        if(p2 == null)
            p2 =  GetBigPrime.getBigPrime(len);
        return p2;
    }

    private static BigInteger getN(int len) {
        return getP1(len).multiply(getP2(len));
    }

    private static int getK(BigInteger fn) {
        BigInteger bk;
        for (int k = 1;; k++) {
            bk = new BigInteger(k + "");
            if((((fn.multiply(bk)).add(BigInteger.ONE)).remainder(E)).equals(BigInteger.ZERO)) {
                return k;
            }
            if(k >= 1000)
                return -1;
        }
    }

    private static BigInteger getD(BigInteger fn, BigInteger bk) {
        return ((bk.multiply(fn)).add(BigInteger.ONE)).divide(E);
    }

    /**
     * 获取随机的公钥和私钥
     * @param len p1, p2 的长度
     */
    public static void getKey(int len) {
        BigInteger fn = (getP1(len).subtract(BigInteger.ONE)).multiply(getP2(len).subtract(BigInteger.ONE));
        int k;
        while((k = getK(fn)) == -1) {
            p1 = null;
            p2 = null;
            fn = (getP1(len).subtract(BigInteger.ONE)).multiply(getP2(len).subtract(BigInteger.ONE));
        }
        BigInteger bk = new BigInteger(k + "");
        BigInteger d = getD(fn, bk);
        BigInteger n = getN(len);
        D = d;
        N = n;
        System.out.println("公钥：（ e = " + E + ", n = " + N + "）");
        System.out.println("私钥：（ d = " + D + ", n = " + N + "）");
    }

    @SuppressWarnings("all")
    public static String encode(String text, String pkE, String pkN) {
        BigInteger bpkN = new BigInteger(pkN);
        BigInteger bpkE = new BigInteger(pkE);
        List<BigInteger> bigIntegersTexts = StrBit.stringToBigInt(text);
//        System.out.println(bigIntegersTexts);
        List<BigInteger> result = new LinkedList<>();
        for (BigInteger bigIntegersText : bigIntegersTexts) {
            result.add((bigIntegersText.pow(bpkE.intValue())).mod(bpkN));
        }
//        System.out.println("加密后的：" + result);
        return StrBit.bigIntToString(result);
    }

    @SuppressWarnings("all")
    public static String decode(String cipherText, String pkD, String pkN) {
        // TODO: 汉语解码出错
        BigInteger bpkN = new BigInteger(pkN);
        BigInteger bpkD = new BigInteger(pkD);
        List<BigInteger> cipherTexts = StrBit.stringToBigInt(cipherText);
//        System.out.println("解密前：" + cipherTexts);
        List<BigInteger> result = new LinkedList<>();
        for (BigInteger text : cipherTexts) {
            BigInteger mod = (text.pow(bpkD.intValue())).mod(bpkN);
            result.add(mod);
        }
//        System.out.println("解密出的bigInteger: " + result);
        return StrBit.bigIntToString(result);
    }

    public static void main(String[] args) {

//        getKey(2);

        String e = "3";
        String n = "1081";
        String d = "675";
        System.out.println("加密后的结果： " + encode("junebao.top", e, n));
        System.out.println("解密后的结果： " + decode("̓ʌġl˒ĵ¦.ϵ¦˅", d, n));
    }
}

```

字符串与二进制转换 [参考](https://www.cnblogs.com/StanLong/p/6906814.html)

```java
package top.junebao;

import java.math.BigInteger;
import java.util.LinkedList;
import java.util.List;

public class StrBit {

    /**
     * 将一个字符串转换为二进制串，再转化为BigInteger
     * https://www.cnblogs.com/StanLong/p/6906814.html
     * @param str 要转换的字符串
     * @return 返回一个List容器，包含转换得到的BigInteger
     */
    public static List<BigInteger> stringToBigInt(String str) {
        LinkedList<BigInteger> bill = new LinkedList<>();
        char[] strChar = str.toCharArray();
        for (char c : strChar) {
            bill.add(new BigInteger(Integer.parseUnsignedInt(Integer.toBinaryString(c),2) + ""));
        }
        return bill;
    }

    //将二进制字符串转换成int数组
    private static int[] binStrToIntArray(String binStr) {
        char[] temp=binStr.toCharArray();
        int[] result=new int[temp.length];
        for(int i=0;i<temp.length;i++) {
            result[i]=temp[i]-48;
        }
        return result;
    }


    //将二进制转换成字符
    private static char binStrToChar(String binStr){
        int[] temp=binStrToIntArray(binStr);
        int sum=0;
        for(int i=0; i<temp.length;i++){
            sum +=temp[temp.length-1-i]<<i;
        }
        return (char)sum;
    }

    /**
     * 将BigInteger容器中的数拿出来转换为字符串
     * https://www.cnblogs.com/StanLong/p/6906814.html
     * @param bigIntegers 一个容器对象，包含BigInteger数据
     * @return 返回转换后的字符串
     */
    public static String bigIntToString(List<BigInteger> bigIntegers){
        StringBuilder sb = new StringBuilder();
        for (BigInteger bigInteger : bigIntegers) {
            sb.append(binStrToChar(bigInteger.toString(2)));
        }
        return sb.toString();
    }


    public static void main(String[] args) {
        System.out.println(stringToBigInt("张君保"));
        System.out.println(bigIntToString(stringToBigInt("张君保")));
    }
}

```

