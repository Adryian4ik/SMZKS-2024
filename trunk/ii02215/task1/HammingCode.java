import java.util.Arrays;

public class HammingCode {
    private static int r = 0;

    public static int[] encodeHammingCode(int number) {
        String binaryNumber = Integer.toBinaryString(number);
        int dataLength = binaryNumber.length();

        r = 0;
        while (Math.pow(2, r) < (dataLength + r + 1)) {
            r++;
        }
        int codeLength = dataLength + r;

        int XOR = 0;
        int[] code = new int[codeLength];

        for (int i = 0, j = 0; i < codeLength; i++) {
            if (Math.log(i + 1) / Math.log(2) == Math.floor(Math.log(i + 1) / Math.log(2))) {
                code[i] = 0;
            } else {
                code[i] = Character.getNumericValue(binaryNumber.charAt(j++));
                if (code[i] == 1) {
                    XOR ^= i + 1;
                }
            }
        }

        String str = Integer.toBinaryString(XOR);
        while (str.length() < r) {
            str = "0" + str;
        }

        for (int i = 0; i < r; i++) {
            int position = (int) Math.pow(2, i);
            code[position - 1] = Integer.parseInt(String.valueOf(str.charAt(i)));
        }

        System.out.print("\nGenerated Hamming Code:\n");
        Arrays.stream(code).forEach(System.out::print);
        System.out.println();
        return code;
    }

    public static void checkHammingCode(int[] code) {
        int XOR = 0;

        for (int i = 0; i < code.length; i++) {
            if (code[i] == 1) {
                XOR ^= i + 1;
            }
        }

        if (XOR != 0) {
            System.out.println("Error detected at position: " + XOR);
            code[XOR - 1] ^= 1;
            System.out.print("Corrected Hamming Code: ");
            Arrays.stream(code).forEach(System.out::print);
            System.out.println("\n");
        } else {
            System.out.println("No errors detected.");
        }
    }

    public static int decodeHammingCode(int[] code) {
        StringBuilder dataBits = new StringBuilder();
        for (int i = 0; i < code.length; i++) {
            if (Math.log(i + 1) / Math.log(2) != Math.floor(Math.log(i + 1) / Math.log(2))) {
                dataBits.append(code[i]);
            }
        }
        return Integer.parseInt(dataBits.toString(), 2);
    }


}
