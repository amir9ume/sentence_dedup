# sentence_dedup


A naive Nearest neighbor search without an index involves computing the  distance from the query to each point in the database, which for large datasets is 
computationally prohibitive. For high-dimensional data, HNSW is more suitable.



To achieve high Throughput:

If the application needs to process a large number of sentences in real-time, 
a GPU will provide faster encoding times. We can add a parameter for a small batch size, or a maximum wait time

#Key Requirements
1. The system must process an ordered stream of sentences.

 - This basically means that the older sentences would have arrived first, and we can use a queue, to pop sentences from the front. 

2. Implement a buffer to store previously seen sentences. The buffer size should be
configurable as a parameter in your code.

- We can use a queue data structure to implement buffer, with some size value buffer_size
  
● The system must handle varying buffer sizes, ranging from tens to thousands of
sentences.

- If size is a parameter, we should be able to do it for any size
  
4. It should process new sentences quickly, maintaining low latency even as the buffer grows to
its maximum size.


5. The system should balance accuracy of semantic similarity detection with processing speed.

 
# Assumptions

The approach and design decisions are: 

- How your system handles different buffer sizes
Answer:

- Any assumptions made about the nature of the incoming stream
Answer:Current sentence transformer model based on BERT has 512 tokens limitation. If we get sentences or paragraphs, longer than 512 tokens, we would need to change the encoder model.

- Potential optimizations for scaling to larger buffer sizes
Answer:

- How you balance the trade-off between comparison accuracy and processing speed
Answer:
Simpler models like distilBert or others can improve speed of emedding, but it can come at cost of accuracy
We can increase the threshold for similarity, which would mean a faster search, but we can miss out on many semantically duplicate sentences.


3. An overview of how you envision this component being deployed and integrated in a
streaming data pipeline.
Answer
