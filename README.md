# Implied Volatility API
This API is used to service a kubernetes cluster on GCP. The API partitions work (set of stock symbols) to a set of worker nodes that then collect data based on the stock symbols passed to them. 

Previously, this API ran inside the same pod as the data collection code that makes external requests to stock data APIs. Some APIs that I use to collect data (IEX Cloud) have an IP based rate limit, significantly slowing down the time it takes to collect data for each stock symbol. Additionally, the previous setup could not be scaled horiontally very well since each copy of the code running in the cloud would need access to the database pretty much at the same time. 

To resolve the IP based rate limit, the client data collection code runs in its own kubernetes pod. This is an advantage because each pod has its own IP address and will only be limited by its own calls, and not by the rate of calls made by other worker nodes.

The database access issue was resolved by creating a queue and submitting data to be saved to the database via the queue. The queue would process data to be saved at a rate that does not overload the database. 

