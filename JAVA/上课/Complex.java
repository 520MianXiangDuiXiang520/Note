public class Complex {
    float imaginary;
    float real;

    public Complex(float real,float imaginary){
        this.imaginary = imaginary;
        this.real = real;
    }

    public static Complex add(Complex x1,Complex x2){
        return new Complex(x1.real + x2.real, x1.imaginary + x2.imaginary);
    }

    public static Complex less(Complex x1,Complex x2){
        return new Complex(x1.real - x2.real, x1.imaginary - x2.imaginary);
    }

    public static Complex multipy(Complex x1,Complex x2){
        return new Complex(x1.real * x2.real, x1.imaginary * x2.imaginary);
    }

    public static Complex except(Complex x1,Complex x2){
        return new Complex(x1.real / x2.real, x1.imaginary / x2.imaginary);
    }

    public static void sout(Complex x1){
        if(x1.imaginary < 0){
            if(x1.imaginary == -1){
                System.out.println(x1.real + "-i");
            }else{
                System.out.println(x1.real +""+ x1.imaginary + "i");
            }

        }else{
            if(x1.imaginary == 1){
                System.out.println(x1.real + "+i");
            }else{
                System.out.println(x1.real + "+" + x1.imaginary + "i");
            }
        }
    }
    public static void main(String[] args) {
        Complex c1 = new Complex(1,2);
        Complex c2 = new Complex(2,3);
        sout(add(c1,c2));
        sout(less(c1,c2));
        sout(multipy(c1, c2));
        sout(except(c1, c2));
//        3.0+5.0i
//        -1.0-i
//        2.0+6.0i
//        0.5+0.6666667i
    }
}
