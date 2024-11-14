import java.math.BigInteger;

public class Main{
    public static void main(String[] args) {

        BigInteger N = new BigInteger("99595193774911");
        BigInteger e = new BigInteger("1908299");
        BigInteger[] CValues = {
                new BigInteger("75790643190143"),
                new BigInteger("36869061035180"),
                new BigInteger("38422576553598"),
                new BigInteger("68899435645717"),
                new BigInteger("16193161920958"),
                new BigInteger("98487458352335"),
                new BigInteger("34167725433806"),
                new BigInteger("96613844267045"),
                new BigInteger("26583768908805"),
                new BigInteger("73052827576371"),
                new BigInteger("94695336463618"),
                new BigInteger("69092596694070")
        };

        MethodFermat methodFermat = new MethodFermat(N, e);

        for (BigInteger C : CValues) {
            System.out.println("Обработка C = " + C);
            methodFermat.checkSqrt(C);
        }


/*        BigInteger N = new BigInteger("65815671868057");
        BigInteger e = new BigInteger("7423489");
        BigInteger C = new BigInteger("38932868535359");

        MethodFermat methodFermat = new MethodFermat(N, e, C);
        methodFermat.checkSqrt(N);

        BigInteger result = methodFermat.sqrt(N);*/
    }
}