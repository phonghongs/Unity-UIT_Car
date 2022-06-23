using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading;
using System.Net.Sockets;
using System.Net;
using System;
using System.Text;
using Newtonsoft.Json;

/*
    Client                                  ServerMessage
    ______________________________________________________________
    CMD :   Function                        CMD :   Function
    1   :   SetController                   1   :   VehicleStage
    2   :   GetImage                        2   :   OriginalImage
    3   :   GetImage                        3   :   SegmentImage
*/

public class SetController
{
    public short Cmd {
        get;
        set;
    }
    public float Speed {
        get;
        set;
    }
    public float Angle {
        get;
        set;
    }
}

public class GetImage
{
    public short Cmd {
        get;
        set;
    }
}

public class VehicleStage
{
    public short Cmd {
        get;
        set;
    }
    public float Speed {
        get;
        set;
    }
    public float Angle {
        get;
        set;
    }
    public float Lat {
        get;
        set;
    }
    public float Lon {
        get;
        set;
    }
    public float Heading {
        get;
        set;
    }
}

public class OriginalImage
{
    public short Cmd {
        get;
        set;
    }
    public byte[] Original {
        get;
        set;
    }
}

public class SegmentImage
{
    public short Cmd {
        get;
        set;
    }
    public byte[] Segment {
        get;
        set;
    }
}

public class serversocket : MonoBehaviour
{
    private bool mRunning;
    private Thread mThread;
    private TcpListener tcp_Listener = null;
    private string remoteIp = "0.0.0.0";
    private int remotePort = 11000;
    public sceneController camController;

    void Start()
    {
        string jsonData = @"
                        {
                            'Cmd': 12,
                            'abc': 13
                        }";
        var myDetails = JsonConvert.DeserializeObject < SetController > (jsonData);
        Debug.Log(string.Concat("Hi ", myDetails.Cmd));
        RestartServer();
    }

    void RestartServer()
    {
        stopListening();
        mRunning = true;
        ThreadStart ts = new ThreadStart(StartListening);
        mThread = new Thread(ts);
        mThread.Start();
    }

    bool SocketConnected(Socket s)
    {
        bool part1 = s.Poll(1000, SelectMode.SelectRead);
        bool part2 = (s.Available == 0);
        if (part1 && part2)
            return false;
        else
            return true;
    }

    public void stopListening()
    {
        mRunning = false;
    }

    void StartListening()
    {
        try
        {
            Debug.Log("Before Started at host:"+remoteIp+", port "+remotePort);
            tcp_Listener = new TcpListener(IPAddress.Any, remotePort); //System.Net.IPAddress
            tcp_Listener.Start();
            Debug.Log("Server Started at host:"+remoteIp+", port "+remotePort);

            // Buffer for reading data

            Byte[] bytes = new Byte[256];
            String jsonData = null;

            while (mRunning)
            {
                // check if new connections are pending, if not, be nice and sleep 100ms
                if (!tcp_Listener.Pending())
                {
                    Thread.Sleep(100);
                }
                else
                {
                    TcpClient client = tcp_Listener.AcceptTcpClient();
                    NetworkStream stream = client.GetStream();

                    int i = 0;
                    jsonData = null;
                    byte[] msg = null;
                    // Loop to receive all the data sent by the client.

                    while((i = stream.Read(bytes, 0, bytes.Length))!=0)
                    {
                        jsonData = System.Text.Encoding.ASCII.GetString(bytes, 0, i);
                        var myDetails = JsonConvert.DeserializeObject < SetController > (jsonData);
                        String returnMessage = "";
                        switch (myDetails.Cmd)
                        {
                            case 1:
                                var VehicleStage_ = new VehicleStage{
                                    Cmd = 1,
                                    Speed = 0.0f,
                                    Angle = 0.0f,
                                    Lat = 0.0f,
                                    Lon = 0.0f,
                                    Heading = 0.0f
                                };
                                returnMessage = JsonConvert.SerializeObject(VehicleStage_);
                                msg = Encoding.UTF8.GetBytes(returnMessage);
                                break;

                            case 2:
                                msg = camController.imageResult.originalIMG;
                                break;

                            case 3:
                                msg = camController.imageResult.segmentIMG;
                                break;
                            default:
                            break;
                        }
                        stream.Write(msg, 0, msg.Length);
                    }

                    client.Close();
                    Debug.Log("Client closed" );
                }
            } // while
        }

        catch (ThreadAbortException)
        {
            Debug.Log("Error");
        }
        finally
        {
            mRunning = false;
            tcp_Listener.Stop();
        }
    }

    void OnApplicationQuit()
    {
        // stop listening thread
        stopListening();
        // wait fpr listening thread to terminate (max. 500ms)
        mThread.Join(500);
        tcp_Listener.Stop();
    }
}
