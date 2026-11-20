import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.charset.StandardCharsets;

/** Sends 10,000 numbered UDP datagrams without waiting for ACKs. */
public class BurstSender {
    private static final int TOTAL = 10000;

    /** Takes the destination address and port as command-line arguments. */
    public static void main(String[] args) throws IOException {
        InetAddress address = InetAddress.getByName(args[0]);
        int port = Integer.parseInt(args[1]);

        try (DatagramSocket socket = new DatagramSocket()) {
            for (int sequence = 0; sequence < TOTAL; sequence++) {
                byte[] data = Integer.toString(sequence).getBytes(StandardCharsets.UTF_8);
                DatagramPacket packet = new DatagramPacket(data, data.length, address, port);
                socket.send(packet);
            }
        }

        System.out.println("Sent: " + TOTAL);
    }
}