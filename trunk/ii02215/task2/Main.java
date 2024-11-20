public class Main{
    public static void main(String[] args){

        int sizeX = 4;
        int sizeY = 4;
        int sizeZ = 0;
        int length = 16;
        int num_parities = 3;


        int num = 46307;

        IterativeCode iterativeCode = new IterativeCode(sizeX, sizeY, sizeZ, length, num_parities);
        iterativeCode.setMatrix(num);
        iterativeCode.introduceError();
        iterativeCode.detectAndFixErrors();
    }
}