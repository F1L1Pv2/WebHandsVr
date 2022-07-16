using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Globalization;

public class Handtracking : MonoBehaviour
{
    public UDPReceive udpReceive;
    public GameObject[] handPoints;

    public GameObject[] LeftHandPoints;
    public GameObject[] RightHandPoints;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        //check type
        string data = udpReceive.data;

        //data = data.Remove(data.Length - 1,1);


        //print(data);

        string[] hands= data.Split(';');

        for (int i = 0; i < hands.Length-1; i++)
        {
            string[] hand = hands[i].Split(':');

            string type = hand[0];
            string pos = hand[1];
            string temp = hand[2];

            temp = temp.Remove(temp.Length - 1, 1);
            temp = temp.Remove(0,1);
            string[] points = temp.Split(',');


            for(int j =0; j<21; j++){
                float pointx = (-(320-float.Parse(points[j*3])))/1000;
                float pointy = (-(240-float.Parse(points[j*3+1])))/1000;
                float pointz = float.Parse(points[j*3+2])/1000;

                if(type == "Left"){
                    LeftHandPoints[j].transform.localPosition = new Vector3(pointx, pointy, pointz);
                }
                else if(type == "Right"){
                    RightHandPoints[j].transform.localPosition = new Vector3(pointx, pointy, pointz);
                }
            }

            //print(type);
           // print(pos);

           pos = pos.Remove(0, 1);
           pos = pos.Remove(pos.Length - 1, 1);

           //print(pos);
           

           string[] posXYZ = pos.Split(',');
           //

           float x = float.Parse(posXYZ[0],CultureInfo.InvariantCulture);
           float y = float.Parse(posXYZ[1],CultureInfo.InvariantCulture);
           float z = float.Parse(posXYZ[2],CultureInfo.InvariantCulture);

            float newx = x * 0.01f;
            float newy = y * 0.01f;
            
            //float newx = 0;
            //float newy = 0;
            float newz = z * 0.01f;

           if(type == "Left"){
               handPoints[0].transform.localPosition = new Vector3(newx, newy, newz);
           }
           else if(type == "Right"){
               handPoints[1].transform.localPosition = new Vector3(newx, newy, newz);
           }
        
        }

        //print(data);

    }
}
