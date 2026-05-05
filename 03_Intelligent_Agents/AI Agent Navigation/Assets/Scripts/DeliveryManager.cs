using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using Unity.VisualScripting;

public class DeliveryManager : MonoBehaviour
{
    public Queue<Delivery> deliveries = new Queue<Delivery>();
    public bool collectedPackage;
    public Vector3 startingPosition;
    public Agent agent;
    public GridManager gridManager;
    public GameObject packageVisual;
    public TextMeshProUGUI timerText;
    private float timeElapsed;

    void Start()
    {
        startingPosition = transform.position;
        AddDelivery();
    }

    private void Update()
    {
        if(packageVisual.activeInHierarchy)
        {
            timeElapsed += Time.deltaTime;
        }

        if(timerText)
        {
            timerText.text = "Delivery Time Elapsed: " + timeElapsed.ToString("F0") + "s";
        }

    }

    public void AddDelivery()
    {
        deliveries.Enqueue(new Delivery(gridManager.GetRandomPositionInsideGrid()));
        timeElapsed = 0;
        StartCoroutine(StartDeliverPackage());
    }
    
    public void CancelCurrentDelivery()
    {

        agent.HandleCustomDestination(startingPosition);
    }

    IEnumerator StartDeliverPackage()
    {
        if (timerText)
        {
            timerText.color = Color.white;
        }

        collectedPackage = true;
        packageVisual.SetActive(true);

        agent.HandleCustomDestination(deliveries.Dequeue().destination);
        yield return new WaitForEndOfFrame();
        yield return new WaitUntil(() => !agent.followingPath);

        StartCoroutine(ReturnToStart());
        //agent.OnDestinationReached += ReturnToStart;

    }

    IEnumerator ReturnToStart()
    {
        if (timerText)
        {
            timerText.color = Color.yellow;
        }

        collectedPackage = false;
        packageVisual.SetActive(false);

        agent.HandleCustomDestination(startingPosition);

        yield return new WaitForEndOfFrame();
        yield return new WaitUntil(() => !agent.followingPath);
        
        AddDelivery();
        //agent.OnDestinationReached += StartDeliverPackage;
    }


    public class Delivery
    {
        public Vector3 destination;
        
        public Delivery(Vector3 destination)
        {
            this.destination = destination;
        }
    }

}
