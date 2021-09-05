import java.io.DataOutputStream;
import java.net.Socket;
import java.io.*;

public class communication {
    private Socket s;
    private DataOutputStream dOut;
    private DataInputStream  dIn;

    public boolean connect(String ip, Integer port){
        try {
            s = new Socket(ip,port);
            dOut = new DataOutputStream(s.getOutputStream());
            dIn = new DataInputStream(s.getInputStream());
            return true;
        }
        catch(Exception  e) {
            return false;
        }
    }
    public Boolean disconnect() {
        try{
            dOut.close();
            dIn.close();
            s.close();
            return true;
        }
        catch(Exception  e) {
            return false;
        }
    }
    public Boolean sendMessage(String message) {
        try {

//        	PrintWriter writer = new PrintWriter(dOut, true);
//        	writer.println(message);
//          dOut.flush();

            dOut.writeUTF(message);

            return true;
        }
        catch (Exception e) {
            return false;
        }
    }
    public String getMessage() {
        try {
//            BufferedReader reader = new BufferedReader(new InputStreamReader(s.getInputStream()));
//            StringBuilder builder = new StringBuilder();
//            String line;
//            while ((line = reader.readLine()) != null) {
//            	builder.append(line);
//            }
//
//            return builder.toString();
            return (String)dIn.readUTF();
        }
        catch(Exception  e) {
            return "Error";
        }
    }
}
