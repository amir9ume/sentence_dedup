# Sentence De-duplication System

## Key Requirements for the Task
- The system must process an ordered stream of sentences.
- The buffer size should be configurable as a parameter in your code.
- The system must handle varying buffer sizes, ranging from tens to thousands of sentences.
- It should process new sentences quickly, maintaining low latency even as the buffer grows to its maximum size.
- The system should balance accuracy of semantic similarity detection with processing speed.

## Assumptions

The assumptions we make for this sentence deduplicator are:

- **Assumption about Stream**: Sentences are independent of their context. Semantic meaning of sentence can be captured with the sentence itself.
- For simple code, one sentence comes to be processed at a time to the cache. For scaling in real code, we should send a batch of sentences, to make best use of GPU resources.
- Number of tokens in the sentences is less than equal to 512 tokens. More tokens would change the choice of our encoder model from Sentence BERT to another encoding model.
- Sentences come in ordered fashion. Hence older sentences would have arrived first, and we can use a queue (FIFO), to pop sentences from the front.
- Accuracy of semantic similarity detection depends on choice of encoder and threshold. Simpler models like distilBert or other lightweight models can improve speed of embedding, but it will come at the cost of accuracy.

## Design

- We initialize a buffer of some desired size. A queue/deque data structure is very useful for it, to pop out old sentences based on FIFO. We can think of an LRU cache too, but I will keep things simpler here.
- We can make use of FAISS or QDRANT libraries for query embeddings similarity check.
- New incoming sentences are checked if they are already present in the buffer hashmap. If not, then they are embedded with a choice of encoder.
- The embedded sentence can then be checked for semantic similarity with previously embedded sentences, using a similarity threshold. If an embedded sentence is closer in similarity than the threshold, we don’t add it to the cache. And we ignore this sentence as a duplicate.
- If the embedded sentence was not close to any of the previous embeddings, we add it to the embedded cache.

### Potential Optimizations for Scaling to Larger Buffer Sizes
- We can implement a batching system for embedding the sentences. The batch size can be a small enough value (for example 8), where we wait for those many samples to collect before sending them to the GPU. We can also implement a wait time limit, to make sure we don’t wait too long, if the batch size samples were not collected within the time limit.

## How to Balance the Trade-off Between Comparison Accuracy and Processing Speed

- Accuracy of semantic similarity detection depends on choice of encoder and threshold. Simpler models like distilBert or other lightweight models can improve speed of embedding, but it will come at the cost of accuracy.
- If we decrease the similarity threshold, then more new sentences will be classified as similar to past sentences, and the cache will not get appended with newer embeddings. This implies a smaller search space for the querying algorithm, and hence faster returns.

## Overview of How This Component Can Be Deployed and Integrated in a Streaming Data Pipeline

- We can use a tokenizer running on distributed servers to tokenize in parallel. (tokenizer service).
- We can have a service running for the encoder model. It expects tokens, and returns embeddings. This service should have GPU resources attached to it.
- In between the tokenizer service and the encoder service, we will implement the cache for de duplication.

## How This Component Can Be Deployed and Integrated into a Larger Streaming Data Pipeline

- To scale it for larger streaming data, we can have a queue service (message broker like rabbit mq or kafka), in between the sentence tokenization and embedding. This ensures data resiliency and scalability.
- If we decrease the similarity threshold, then more new sentences will be classified as similar to past sentences, and the cache will not get appended with newer embeddings. This implies a smaller search space for the querying algorithm, and hence faster returns.

## Efficient Data Structure and Algorithm to Store and Query the Buffer of Previous Sentences

- We can use a queue/deque data structure along with hashmap to implement a cache buffer, with a buffer_size value as parameter at initialization time. We can use a queue (FIFO), to pop sentences from the front whenever the buffer capacity is reached. The hashmap data structure can provide O(1) lookup time to check if a sentence is already present.

- A naive Nearest neighbor search without an index involves computing the distance from the query to each point in the database, which for large datasets is computationally prohibitive. For high-dimensional data, HNSW, a more suitable indexing algorithm is much better.

### Potential Optimizations for Scaling to Larger Buffer Sizes
- More memory will be needed for a larger buffer.
- We can choose to do a PCA on the embeddings, or reduce the embedding dimensions, to use less memory per sentence cache. Though this will come at the expense of accuracy.
