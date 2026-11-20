import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;

/** Counts received datagrams and calculates the loss rate. */
public class BurstReceiver {
    private static final int TOTAL = 10000;

    /** Takes the listening port and the pause in milliseconds. */
    public static void main(String[] args) throws IOException, InterruptedException {
        int port = Integer.parseInt(args[0]);
        int pauseMs = Integer.parseInt(args[1]);

        boolean[] seen = new boolean[TOTAL];
        int received = 0;
        byte[] buffer = new byte[32];

        try (DatagramSocket socket = new DatagramSocket(port)) {
            socket.setSoTimeout(30000);
            System.out.println("Ready. Start the sender within 30 seconds.");

            while (received < TOTAL) {
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);

                try {
                    socket.receive(packet);
                } catch (SocketTimeoutException e) {
                    break;
                }

                String text = new String(
                        packet.getData(), 0, packet.getLength(), StandardCharsets.UTF_8
                );
                int sequence = Integer.parseInt(text);

                if (received == 0) {
                    // After the burst starts, stop after two seconds without a packet.
                    socket.setSoTimeout(2000);
                }

                // Count each sequence number only once.
                if (!seen[sequence]) {
                    seen[sequence] = true;
                    received++;
                }

                if (pauseMs > 0) {
                    Thread.sleep(pauseMs);
                }
            }
        }

        int lost = TOTAL - received;
        double lossRate = 100.0 * lost / TOTAL;

        System.out.println("Received: " + received);
        System.out.println("Lost: " + lost);
        System.out.printf("Loss rate: %.2f%%%n", lossRate);
    }
}