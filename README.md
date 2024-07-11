# sentence_dedup


A naive Nearest neighbor search without an index involves computing the  distance from the query to each point in the database, which for large datasets is 
computationally prohibitive. For high-dimensional data, HNSW is more suitable.



To achieve high Throughput:

If the application needs to process a large number of sentences in real-time, 
a GPU will provide faster encoding times. We can add a parameter for a small batch size, or a maximum wait time
 
