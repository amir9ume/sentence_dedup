import time
import random
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import torch
from collections import deque

class SemanticDeduper:
    def __init__(self, buffer_size=1000, similarity_threshold=0.8, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = device
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2', device=self.device)
        self.buffer_size = buffer_size
        self.similarity_threshold = similarity_threshold
        self.sentences = deque()
        self.embeddings = np.empty((0, 384), dtype=np.float32)  
        self.index = faiss.IndexHNSWFlat(384, 32)  #HNSW index for faster search
        self.seen_sentences = {} 
        

    def encode_sentence(self, sentence):
        embedding = self.model.encode([sentence], convert_to_tensor=True, device=self.device)
        return embedding.cpu().numpy()[0]

    def add_to_buffer(self, sentence, embedding):
        if len(self.sentences) < self.buffer_size:
            self.sentences.append(sentence)
            self.embeddings = np.vstack([self.embeddings, embedding])
            self.index.add(np.array([embedding]))
        else:
            self.sentences.popleft()
            self.embeddings = self.embeddings[1:]
            self.sentences.append(sentence)
            self.embeddings = np.vstack([self.embeddings, embedding])
            self.index = faiss.IndexHNSWFlat(384, 32)  
            self.index.add(self.embeddings)

    def is_duplicate(self, embedding):
        D, I = self.index.search(np.array([embedding]), 1)
        if D[0][0] < self.similarity_threshold:
            return True
        return False

    def process_sentence(self, sentence):
        if sentence in self.seen_sentences:
            print(f"Exact duplicate sentence: {sentence}")
            return
        embedding = self.encode_sentence(sentence)
        #PCA can be added here, if we want to reduce the memory usage of embeddings
        if not self.is_duplicate(embedding):
            self.seen_sentences[sentence] = True
            self.add_to_buffer(sentence, embedding)
            print(f"New sentence: {sentence}")
        else:
            print(f"Semantic duplicate sentence: {sentence}")

    def process_stream(self, stream):
        for sentence in stream:
            self.process_sentence(sentence)
            time.sleep(random.uniform(0.01, 0.1))  # Simulate variable stream rate

buffer_size = 1000
similarity_threshold = 0.8

deduper = SemanticDeduper(buffer_size, similarity_threshold)

stream = [
    "The quick brown fox jumps over the lazy dog.",
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "A journey of a thousand miles begins with a single step.",
    "The quick brown fox jumped over the lazy dog.",
    "The quick brown fox jumps over a lazy dog.",
    "A journey of a thousand miles starts with a single step.",
    "A journey of a thousand miles begins with one step.",
    "The speedy brown fox leaps over the sleepy dog.",
    "Traveling a thousand miles starts with the first step.",
    "An expedition of a thousand miles begins with one step.",
    "The quick brown fox hops over the tired dog.",
    "The weather today is sunny with a chance of rain.",
    "Machine learning is a fascinating field of study.",
    "Python is a versatile programming language used in many industries.",
    "Artificial intelligence is transforming the world rapidly.",
    "In the midst of a bustling city, a small café stands as a serene oasis where people come to relax and enjoy a cup of coffee.",
    "The conference on artificial intelligence attracted experts from around the globe, each eager to share their latest research and developments.",
    "During the summer, the beautiful beaches attract tourists who enjoy the warm sun and the refreshing ocean waves.",
    "The historical museum offers a glimpse into the past with its extensive collection of artifacts and exhibits."
]

deduper.process_stream(stream)
