from sentence_transformers import SentenceTransformer

def generate_search_embedding(search, model='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model)
    vector = model.encode(search)
    return vector
