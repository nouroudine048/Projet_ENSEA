import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.nio.charset.StandardCharsets;


public class UDPClient {

    public static void main(String[] args) throws IOException {
        if (args.length != 2) {
            System.err.println("Usage: java UDPClient <server-address> <port>");
            return;
        }

        InetAddress serverAddress = InetAddress.getByName(args[0]);
        int serverPort = Integer.parseInt(args[1]);

        sendMessages(serverAddress, serverPort);
    }

   
    /** Reads each line, numbers it, and sends it to the server. */
private static void sendMessages(InetAddress serverAddress, int serverPort)
        throws IOException {
    try (DatagramSocket socket = new DatagramSocket();
         BufferedReader input = new BufferedReader(
                 new InputStreamReader(System.in, StandardCharsets.UTF_8))) {

        // Limit each wait for an ACK to 500 ms.
        socket.setSoTimeout(500);

        System.out.println("Type a message and press Enter.");

        int sequence = 0;
        String message;

        while ((message = input.readLine()) != null) {
            // Put the sequence number before the message text.
            String numberedMessage = sequence + ":" + message;
            byte[] data = numberedMessage.getBytes(StandardCharsets.UTF_8);

            DatagramPacket packet = new DatagramPacket(
                    data, data.length, serverAddress, serverPort
            );

            // Retries use the same number. Only a new message gets a new one.
            sendWithAck(socket, packet, sequence);
            sequence++;
        }
    }
}


    /** Sends a datagram and retries if the matching ACK does not arrive. */
private static void sendWithAck(DatagramSocket socket, DatagramPacket packet,
                               int sequence) throws IOException {
    String expectedAck = "ACK:" + sequence;
    byte[] buffer = new byte[32];

    for (int attempt = 1; attempt <= 3; attempt++) {
        socket.send(packet);
        System.out.println("Sent message " + sequence + ", attempt " + attempt);

        try {
            while (true) {
                DatagramPacket reply = new DatagramPacket(buffer, buffer.length);
                socket.receive(reply);

                String ack = new String(
                        reply.getData(), 0, reply.getLength(), StandardCharsets.UTF_8
                );

                if (ack.equals(expectedAck)) {
                    System.out.println("Received " + ack);
                    return;
                }
            }
        } catch (SocketTimeoutException e) {
            System.out.println("Timeout waiting for " + expectedAck);
        }
    }

    System.out.println("No ACK after 3 attempts for message " + sequence);
}



}