import java.net.*;
import java.nio.charset.StandardCharsets;
import java.io.IOException;


public class UDPServer {

    public int port;
    public DatagramSocket socket;
    public int buffer_size;


    //a constructor taking as argument the listening port of the server;
    public UDPServer(int port, int buffer_size){
        this.port=port;
        this.buffer_size=buffer_size;
    }

    //a default constructor, which uses a default port (e.g. 8080);

    public UDPServer() {
        this.port=8080;
        this.buffer_size=1024;

    }

   /** Receives UDP messages and simulates lost datagrams and ACKs. */
public void launch() {
    try {
        socket = new DatagramSocket(port);
        System.out.println(this);

        byte[] buffer = new byte[buffer_size];
        boolean[] seen = new boolean[10000];
        int expected = 0;

        double dataLossRate = 0.20;
        double ackLossRate = 0.20;

        while (true) {
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            socket.receive(packet);

            // Act as if this datagram never arrived.
            if (Math.random() < dataLossRate) {
                System.out.println("Simulated data loss");
                continue;
            }

            String msg = new String(
                    packet.getData(), 0, packet.getLength(), StandardCharsets.UTF_8
            );

            int separator = msg.indexOf(':');
            if (separator <= 0) {
                System.out.println("Missing sequence number");
                continue;
            }

            int sequence;
            try {
                sequence = Integer.parseInt(msg.substring(0, separator));
            } catch (NumberFormatException e) {
                System.out.println("Invalid sequence number");
                continue;
            }

            if (sequence < 0 || sequence >= seen.length) {
                System.out.println("Sequence number out of range: " + sequence);
                continue;
            }

            if (seen[sequence]) {
                System.out.println("Duplicate message " + sequence);
            } else {
                // Remember the message even if its ACK is lost.
                seen[sequence] = true;

                if (sequence > expected) {
                    System.out.println("Gap: expected " + expected + ", received " + sequence);
                } else if (sequence < expected) {
                    System.out.println("Out-of-order message: " + sequence);
                }

                if (sequence >= expected) {
                    expected = sequence + 1;
                }

                String message = msg.substring(separator + 1);
                System.out.printf("[%s:%d] %d: %s%n",
                        packet.getAddress().getHostAddress(),
                        packet.getPort(),
                        sequence,
                        message);
                System.out.println("Received bytes: " + packet.getLength());

                // Skip the first ACK sometimes to trigger a retry.
                if (Math.random() < ackLossRate) {
                    System.out.println("Simulated loss of ACK:" + sequence);
                    continue;
                }
            }

            // A duplicate still needs an ACK, but we don't print its text again.
            byte[] ackData = ("ACK:" + sequence).getBytes(StandardCharsets.UTF_8);
            DatagramPacket ackPacket = new DatagramPacket(
                    ackData, ackData.length, packet.getAddress(), packet.getPort()
            );
            socket.send(ackPacket);
        }
    } catch (IOException e) {
        if (socket != null) {
            socket.close();
        }
        System.err.println("UDP server error: " + e.getMessage());
    }
}


@Override
public String toString() {
    boolean running = false;

    if (socket != null) {
        running = !socket.isClosed();
    }

    return "UDPServer{port=" + port + ", running=" + running + "}";
}

public static void main(String[] args) throws IOException {
    UDPServer server;

    if (args.length == 0) {
        server = new UDPServer();
    } else {
        int port = Integer.parseInt(args[0]);
        int buffer_size = 1024;

        if (args.length >= 2) {
            buffer_size = Integer.parseInt(args[1]);
        }

        server = new UDPServer(port, buffer_size);
    }

    server.launch();

}

}