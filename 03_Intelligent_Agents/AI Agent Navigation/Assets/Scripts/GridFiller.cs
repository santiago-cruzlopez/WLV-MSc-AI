using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridFiller : MonoBehaviour
{
    public GameObject[] housesPrefabs;
    public GameObject[] decorationPrefabs;

    public void CreateHousesOnNodes(List<Node> slots)
    {
        foreach(Node node in slots)
        {
            if(!node.occupied && !node.walkable)
            {
                GameObject randomHouse = housesPrefabs[Random.Range(0, housesPrefabs.Length)];
                GameObject clonedHouse = Instantiate(randomHouse);
                clonedHouse.transform.position = node.worldPosition;
                clonedHouse.transform.eulerAngles = new Vector3(0, 90 * Random.Range(0, 4), 0);
                node.occupied = true;
            }
        }
    }
}
