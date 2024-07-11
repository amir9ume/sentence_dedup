import time
import random
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class SemanticDeduper:
    def __init__(self, buffer_size=1000, similarity_threshold=0.8):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.buffer_size = buffer_size
        self.similarity_threshold = similarity_threshold
        self.sentences = []
        self.embeddings = np.empty((0, 384), dtype=np.float32)  # Assuming 384-dimensional embeddings
        self.index = faiss.IndexFlatL2(384)  # Use L2 distance

    def add_to_buffer(self, sentences, embeddings):
        if len(self.sentences) < self.buffer_size:
            self.sentences.extend(sentences)
            self.embeddings = np.vstack([self.embeddings, embeddings])
            self.index.add(embeddings)
        else:
            excess = len(self.sentences) + len(sentences) - self.buffer_size
            self.sentences = self.sentences[excess:] + sentences
            self.embeddings = np.vstack([self.embeddings[excess:], embeddings])
            self.index = faiss.IndexFlatL2(384)  # Reset the index
            self.index.add(self.embeddings)

    def is_duplicate(self, embedding):
        D, I = self.index.search(np.array([embedding]), 1)
        if D[0][0] < self.similarity_threshold:
            return True
        return False

    def process_sentences(self, sentences):
        embeddings = self.model.encode(sentences, batch_size=32)  # Encode in batches of 32
        new_sentences = []
        new_embeddings = []
        for sentence, embedding in zip(sentences, embeddings):
            if not self.is_duplicate(embedding):
                new_sentences.append(sentence)
                new_embeddings.append(embedding)
                print(f"New sentence: {sentence}")
            else:
                print(f"Duplicate sentence: {sentence}")
        if new_embeddings:
            self.add_to_buffer(new_sentences, np.array(new_embeddings))

    def process_stream(self, stream, batch_size=32):
        batch = []
        for sentence in stream:
            batch.append(sentence)
            if len(batch) >= batch_size:
                self.process_sentences(batch)
                batch = []
            time.sleep(random.uniform(0.01, 0.1))  # Simulate variable stream rate
        if batch:
            self.process_sentences(batch)

# Example usage
buffer_size = 1000
similarity_threshold = 0.8
deduper = SemanticDeduper(buffer_size, similarity_threshold)

# Simulating a stream of sentences
stream = ["Sentence 1", "Sentence 2", "Sentence 3", "Sentence 1", "Sentence 4"]
deduper.process_stream(stream, batch_size=32)
