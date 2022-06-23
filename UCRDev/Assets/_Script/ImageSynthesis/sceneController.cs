using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class sceneController : MonoBehaviour
{
    public ImageSynthesis synth;
    public ImageSynthesis.CaptureResult imageResult;
    public GameObject[] prefabs;
    public int maxObjects = 10;
    public int height = 480;
    public int width = 640;
    private GameObject[] created;
    private Shapepool pool;
    private int framecount = 0;
    // Start is called before the first frame update
    void Start()
    {
        pool = Shapepool.Create(prefabs);
    }

    // Update is called once per frame
    void Update()
    {
        if (framecount % 30 == 0) {
            GenerateRandom();
        }
        framecount ++;

        // string filename = $"image_{framecount.ToString().PadLeft(5, '0')}";
        // synth.Save(filename, 512, 512, "image");
        imageResult = synth.GetImageResult(width, height);
    }

    void GenerateRandom() {
        pool.ReclaimAll();

        for (int i = 0; i < maxObjects; i++){
            int perfabIndx = Random.Range(0, prefabs.Length);
            GameObject prefab = prefabs[perfabIndx];

            float newX, newY, newZ;
            newX = Random.Range(-10.0f, -10.0f);
            newY = Random.Range(-2.0f, 10.0f);
            newZ = Random.Range(-8.0f, 6.0f);

            Vector3 newPos = new Vector3(newX, newY, newZ);

            var newRot = Random.rotation;

            var shape = pool.Get((ShapeLabel)perfabIndx);
            var newObj = shape.obj;
            newObj.transform.position = newPos;
            newObj.transform.rotation = newRot;

            float xs = Random.Range(0.5f, 4.0f);
            Vector3 newScale = new Vector3(xs, xs, xs);
            newObj.transform.localScale = newScale;

            //color
            float newR, newG, newB;
            newR = Random.Range(0.0f, 1.0f);
            newG = Random.Range(0.0f, 1.0f);
            newB = Random.Range(0.0f, 1.0f);

            var newColor = new Color(newR, newG, newB);
            newObj.GetComponent<Renderer>().material.color = newColor;
        }
        synth.OnSceneChange();
    }
}
