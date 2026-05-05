using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridManager : MonoBehaviour
{
    public LayerMask walkableLayer;
    public LayerMask occupiedLayer;
    public Vector2 gridWorldSize;
    public float nodeRadius;
    public GridFiller gridFiller;

    Node[,] grid;
    public GameObject[] roads = new GameObject[0];

    float nodeDiameter;
    int gridSizeX, gridSizeY;

    void Awake()
    {
        nodeDiameter = nodeRadius * 2;
        gridSizeX = Mathf.RoundToInt(gridWorldSize.x / nodeDiameter);
        gridSizeY = Mathf.RoundToInt(gridWorldSize.y / nodeDiameter);

        CreateGrid();
        FillEmptySlots();

    }
    void FillEmptySlots()
    {
        foreach(Node node in grid)
        {
            if(node.walkable && node.occupied)
            {
                gridFiller.CreateHousesOnNodes(GetNeighbors(node));
            }
        }
    }

    void CreateGrid()
    {
        grid = new Node[gridSizeX, gridSizeY];

        Vector3 worldBottomLeft = transform.position
            - Vector3.right * gridWorldSize.x / 2
            - Vector3.forward * gridWorldSize.y / 2;

        for (int x = 0; x < gridSizeX; x++)
        {
            for (int y = 0; y < gridSizeY; y++)
            {
                Vector3 worldPoint = worldBottomLeft
                    + Vector3.right * (x * nodeDiameter + nodeRadius)
                    + Vector3.forward * (y * nodeDiameter + nodeRadius);

                bool walkable = Physics.CheckSphere(worldPoint, nodeRadius, walkableLayer);
                bool occupied = Physics.CheckSphere(worldPoint, nodeRadius, occupiedLayer);

                grid[x, y] = new Node(walkable, worldPoint, x, y);

                if(occupied)
                {
                    grid[x, y].occupied = occupied;
                }
            }
        }
    }
    public Vector3 GetRandomPositionInsideGrid()
    {
        if(roads.Length == 0)
        {
            roads = GameObject.FindGameObjectsWithTag("Road");
        }

        GameObject randomRoad = roads[Random.Range(0, roads.Length)];

        return randomRoad.transform.position; 
    }
    public Node NodeFromWorldPoint(Vector3 worldPosition)
    {
        float percentX = (worldPosition.x + gridWorldSize.x / 2) / gridWorldSize.x;
        float percentY = (worldPosition.z + gridWorldSize.y / 2) / gridWorldSize.y;

        percentX = Mathf.Clamp01(percentX);
        percentY = Mathf.Clamp01(percentY);

        int x = Mathf.RoundToInt((gridSizeX - 1) * percentX);
        int y = Mathf.RoundToInt((gridSizeY - 1) * percentY);

        return grid[x, y];
    }

    public List<Node> GetNeighbors(Node node)
    {
        List<Node> neighbors = new List<Node>();

        for (int x = -1; x <= 1; x++)
        {
            for (int y = -1; y <= 1; y++)
            {
                if (x == 0 && y == 0)
                    continue;

                int checkX = node.gridX + x;
                int checkY = node.gridY + y;

                if (checkX >= 0 && checkX < gridSizeX &&
                    checkY >= 0 && checkY < gridSizeY)
                {
                    neighbors.Add(grid[checkX, checkY]);
                }
            }
        }

        return neighbors;
    }

    void OnDrawGizmos()
    {
        if (grid == null) return;

        foreach (Node node in grid)
        {
            Gizmos.color = node.walkable ? Color.white : Color.red;
            Gizmos.DrawCube(node.worldPosition, Vector3.one * (nodeDiameter - 0.1f));
        }
    }
}
