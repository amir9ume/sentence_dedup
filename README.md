# sentence_dedup


A naive Nearest neighbor search without an index involves computing the  distance from the query to each point in the database, which for large datasets is 
computationally prohibitive. For high-dimensional data, HNSW is more suitable.



To achieve high Throughput:

If the application needs to process a large number of sentences in real-time, 
a GPU will provide faster encoding times. We can add a parameter for a small batch size, or a maximum wait time
 
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
