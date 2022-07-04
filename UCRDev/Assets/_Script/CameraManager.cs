using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CameraManager : MonoBehaviour
{
    public Button changeVehicles;
    public SocketManager playerCreator;
    public CarFollower camController;
    public GameObject initializeCamera;
    private int playerIndex = 0;

    void Start(){
        camController.carTransform = initializeCamera.GetComponent<Transform>();
        changeVehicles.onClick.AddListener(TaskOnClick);
    }

    void TaskOnClick(){
        playerIndex += 1;
        if (playerIndex >= playerCreator.numPlayer){
            playerIndex = 0;
        }
        playerCreator.SetControllerAvtivate(playerIndex);
        camController.carTransform = playerCreator.players[playerIndex].obj.GetComponent<Transform>();
    }
}
