import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Arrays;

/** Tests UDP payload sizes on the IPv4 loopback address. */
public class DatagramSizeTest {

   
    public static void main(String[] args) throws IOException {
        InetAddress serverAddress = InetAddress.getByName("127.0.0.1");
        int[] sizes = {1000, 10000, 65507, 65508};

        try (DatagramSocket socket = new DatagramSocket()) {
            for (int size : sizes) {
                byte[] data = new byte[size];
                Arrays.fill(data, (byte) 'A');

                DatagramPacket packet = new DatagramPacket(
                        data, data.length, serverAddress, 8080
                );

                try {
                    socket.send(packet);
                    System.out.println("Sent " + size + " bytes");
                } catch (IOException e) {
                    System.out.println("Could not send " + size + " bytes: " + e.getMessage());
                }
            }
        }
    }
}