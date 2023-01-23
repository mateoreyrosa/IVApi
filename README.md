# Implied Volatility API
This API is used to service a kubernetes cluster on GCP. The API partitions work (set of stock symbols) to a set of worker nodes that then collect data based on the stock symbols passed to them. 

## Design
Previously, this API ran inside the same pod as the data collection code that makes external requests to stock data APIs. Some APIs that I use to collect data (IEX Cloud) have an IP based rate limit, significantly slowing down the time it takes to collect data for each stock symbol. Additionally, the previous setup could not be scaled horiontally very well since each copy of the code running in the cloud would need access to the database pretty much at the same time. Previous implementation is here: [Stock Watch](https://github.com/mateoreyrosa/stock_watch)

To resolve the IP based rate limit, the client data collection code runs in its own kubernetes pod. This is an advantage because each pod has its own IP address and will only be limited by its own calls, and not by the rate of calls made by other worker nodes requesting data from the service using the same API key. 

The database access issue was resolved by creating a queue and submitting data to be saved to the database via the queue. The queue would process data to be saved at a rate that does not overload the database. 

## Worker Nodes
The worker node implementation is now proprietary since my trading algorithm actually relies on it. Reach out to me at my [website](https://mateoreyrosa.com) if you would like some high level details about how this is done. 
