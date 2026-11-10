"""Ask RailSeat: retrieval-augmented answers from the travel rules (P10 add-on, task 12).

chunk.py splits the rules, gemini.py talks to the models, index.py stores the
embeddings in pgvector, and retrieve.py finds the nearest rules for a question.
"""
