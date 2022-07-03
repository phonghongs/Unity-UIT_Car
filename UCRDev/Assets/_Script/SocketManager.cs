using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading;
using System.Net.Sockets;
using System.Net;
using System;
using System.Text;
using Newtonsoft.Json;
using System.Net.NetworkInformation;

public class PlayerShape {
    public PrometeoCarController controller;
    public GameObject obj;
}

public class SocketManager : MonoBehaviour
{
    // Start is called before the first frame update

    public GameObject prefab;
    private PlayerShape[] players;
    private bool[] mRunning;
    private Thread[] mThread;
    private TcpListener[] tcp_Listener;
    private int[] remotePort;
    public int numPlayer = 3;

    void Start()
    {
        IPGlobalProperties ipGlobalProperties = IPGlobalProperties.GetIPGlobalProperties();
        TcpConnectionInformation[] tcpConnInfoArray = ipGlobalProperties.GetActiveTcpConnections();
        // Create Player Port
        remotePort = new int[numPlayer];
        int i = 0;
        int baseIP = 11000;
        for (int j = 0; j < numPlayer; j ++){
            bool portOpen =  true;
            while (i < 100 && portOpen) {
                remotePort[j] = baseIP + i;
                foreach (TcpConnectionInformation tcpi in tcpConnInfoArray)
                {
                    if (remotePort[j] == tcpi.LocalEndPoint.Port){
                        portOpen = false;
                        break;
                    }
                }

                i += 1;
                if (!portOpen)
                    portOpen = true;
                else 
                    break;
            }
            Debug.Log(remotePort[j]);
        }

        //Socket repair
        tcp_Listener = new TcpListener[numPlayer];
        mRunning = new bool[numPlayer];
        mThread = new Thread[numPlayer];
        // Create Player instance
        i = 0;
        players = new PlayerShape[numPlayer];
        for (i = 0; i < numPlayer; i++) {
            var obj = Instantiate(prefab, new Vector3(i * 3, i * 3, i * 3), Quaternion.identity);
            obj.GetComponent<PrometeoCarController>().playerCam.depth = i + 1;
            players[i] = new PlayerShape(){
                obj = obj, 
                controller = obj.GetComponent<PrometeoCarController>()
            };
            RestartServer(i);
        }
    }

    public void RestartServer(int serverIndex)
    {
        stopListening(serverIndex);
        mRunning[serverIndex] = true;
        mThread[serverIndex] = new Thread (() => StartListening(serverIndex));
        mThread[serverIndex].Start();
    }

    public void stopListening(int serverIndex)
    {
        mRunning[serverIndex] = false;
    }


    void StartListening(int serverIndex)
    {
        try
        {
            tcp_Listener[serverIndex] = new TcpListener(IPAddress.Any, remotePort[serverIndex]); //System.Net.IPAddress
            tcp_Listener[serverIndex].Start();
            Debug.Log("Server Started at host: localhost, port "+remotePort);

            // Buffer for reading data

            Byte[] bytes = new Byte[256];
            String jsonData = null;

            while (mRunning[serverIndex])
            {
                // check if new connections are pending, if not, be nice and sleep 100ms
                if (!tcp_Listener[serverIndex].Pending())
                {
                    Thread.Sleep(100);
                }
                else
                {
                    TcpClient client = tcp_Listener[serverIndex].AcceptTcpClient();
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
                                PrometeoCarController.VehicleStageCl vhS = players[serverIndex].controller.GetState();
                                var VehicleStage_ = new VehicleStage{
                                    Cmd = 1,
                                    Speed = vhS.crSpeed,
                                    Angle = vhS.crSteering,
                                    Lat = vhS.location.x,
                                    Lon = vhS.location.y,
                                    Heading = vhS.rotation.y
                                };
                                returnMessage = JsonConvert.SerializeObject(VehicleStage_);
                                msg = Encoding.UTF8.GetBytes(returnMessage);
                                break;

                            case 2:
                                msg = players[serverIndex].controller.imageResult.originalIMG;
                                break;

                            case 3:
                                msg = players[serverIndex].controller.imageResult.segmentIMG;
                                break;
                            default:
                            break;
                        }
                        Debug.Log(msg.Length);
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
            mRunning[serverIndex] = false;
            tcp_Listener[serverIndex].Stop();
        }
    }
}
