using UnityEngine;

public class Node
{
    public bool walkable;
    public bool occupied;

    public Vector3 worldPosition;

    public int gridX;
    public int gridY;

    public int gCost;
    public int hCost;
    public Node parent;

    public int fCost
    {
        get { return gCost + hCost; }
    }

    public Node(bool walkable, Vector3 worldPosition, int x, int y)
    {
        this.walkable = walkable;
        this.worldPosition = worldPosition;
        this.gridX = x;
        this.gridY = y;
        this.occupied = walkable;
    }
}