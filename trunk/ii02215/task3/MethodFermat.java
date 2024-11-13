import java.math.BigInteger;

public class MethodFermat {
    private BigInteger N;
    private BigInteger e;

    MethodFermat(BigInteger N, BigInteger e) {
        this.N = N;
        this.e = e;
    }

    public BigInteger sqrt(BigInteger x) {
        if (x.compareTo(BigInteger.ZERO) < 0) {
            throw new ArithmeticException("Cannot compute square root of a negative number");
        }
        if (x.equals(BigInteger.ZERO) || x.equals(BigInteger.ONE)) {
            return x;
        }
        BigInteger a = x;
        BigInteger b = x.shiftRight(1);

        while (b.compareTo(a) < 0) {
            a = b;
            b = x.divide(b).add(b).shiftRight(1); // (x / b + b) / 2
        }

        return a;
    }

    public void checkSqrt(BigInteger C) {
        BigInteger sqrtResult = sqrt(N);
        BigInteger square = sqrtResult.multiply(sqrtResult);

        System.out.println("Корень: " + sqrtResult + " Квадрат корня: " + square + " N: " + N);

        if (square.equals(N)) {
            System.out.println(sqrtResult + " является точным квадратным корнем числа " + N);
        } else {
            System.out.println(sqrtResult + " НЕ является точным квадратным корнем числа " + N);
            BigInteger w1 = square.subtract(N).abs();

            while (!w1.equals(sqrt(w1).multiply(sqrt(w1)))) {
                sqrtResult = sqrtResult.add(BigInteger.ONE);
                square = sqrtResult.multiply(sqrtResult);
                w1 = square.subtract(N).abs();
                System.out.println(sqrtResult + " " + square + " - " + N + " Разность: " + w1 + " квадрат: " + sqrt(w1).multiply(sqrt(w1)) + " Корень: " + sqrt(w1));
            }

            BigInteger p = sqrtResult.add(sqrt(w1));
            BigInteger q = sqrtResult.subtract(sqrt(w1));
            BigInteger Composition = q.subtract(BigInteger.ONE).multiply(p.subtract(BigInteger.ONE));
            System.out.println(sqrtResult + " " + "p: " + p + " q: " + q + " q*p = " + Composition);

            BigInteger inverse = e.modInverse(Composition);
            System.out.println("Обратное к e: " + inverse);

            BigInteger decryptedMessage = C.modPow(inverse, N);
            System.out.println("Исходное сообщение: " + decryptedMessage);

        }
    }


}
