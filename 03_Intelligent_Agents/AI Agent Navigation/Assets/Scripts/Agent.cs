using System;
using System.Collections.Generic;
using Unity.Burst.CompilerServices;
using UnityEngine;

public class Agent : MonoBehaviour
{
    public Pathfinding pathfinding;
    public Animator animations;
    
    public float speed = 5f;
    public bool followingPath;

    public Action OnDestinationReached;
    List<Node> path;
    int targetIndex;

    void Update()
    {
        //HandleMouseInput();
        FollowPath();
    }

    void HandleMouseInput()
    {
        if (Input.GetMouseButtonDown(0))
        {

            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;

            // Make sure your ground has a collider!
            if (Physics.Raycast(ray, out hit))
            {
                path = pathfinding.FindPath(transform.position, hit.point);
                followingPath = true;
                targetIndex = 0;
            }
        }
    }
    public void HandleCustomDestination(Vector3 destination)
    {
        followingPath = true;
        path = pathfinding.FindPath(transform.position, destination);
        targetIndex = 0;
    }

    void FollowPath()
    {
        

        if (path == null || path.Count == 0 || targetIndex >= path.Count)
        {
            if(followingPath && path != null)
            {
                OnDestinationReached?.Invoke();
                animations.SetFloat("Speed", 0);
                followingPath = false;
                path = null;
            }
           

            return;
        }

        

        Vector3 targetPos = path[targetIndex].worldPosition;

        transform.position = Vector3.MoveTowards(
            transform.position,
            targetPos,
            speed * Time.deltaTime
        );

        transform.forward = targetPos - transform.position;

        animations.SetFloat("Speed", speed);
        
        
        if (Vector3.Distance(transform.position, targetPos) < 0.1f)
        {
            targetIndex++;
        }
    }

    void OnDrawGizmos()
    {
        if (path == null) return;

        Gizmos.color = Color.black;

        for (int i = targetIndex; i < path.Count; i++)
        {
            Gizmos.DrawCube(path[i].worldPosition, Vector3.one * 0.3f);

            if (i == targetIndex)
                Gizmos.DrawLine(transform.position, path[i].worldPosition);
            else
                Gizmos.DrawLine(path[i - 1].worldPosition, path[i].worldPosition);
        }
    }   
}