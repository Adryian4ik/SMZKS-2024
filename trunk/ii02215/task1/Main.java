import java.util.Arrays;
import java.util.Scanner;

public class Main{
    public static void main(String[] args){
        int input = 636;
        System.out.println("Entered number: " + input);

        int[] code = HammingCode.encodeHammingCode(input);
        for (int i = 0; i < code.length; i++){
            code[i] ^= 1;
            System.out.printf("Incorrected Hamming Code: ");
            Arrays.stream(code).forEach(System.out::print);
            System.out.printf("\n");
            HammingCode.checkHammingCode(code);
        }

        int decoded = HammingCode.decodeHammingCode(code);
        System.out.println("Decoded number: " + decoded);

        HammingCode.checkHammingCode(code);
    }
}