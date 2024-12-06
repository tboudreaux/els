from sentence_transformers import SentenceTransformer

class fileEmbedder:
    def __init__(self, model='all-MiniLM-L6-v2'):
        self._model = SentenceTransformer(model)
        self._model_name = model
        self._embeddings = dict()

    def embed_single_string(self, string, stringName):
        embedding = self._model.encode(string)
        self._embeddings[stringName] = embedding
        return embedding

    def embed_single_file(self, filename):
        with open(filename, 'r') as file:
            return self.embed_single_string(file.read(), filename)

    def embed_multiple_files(self, filenames):
        embeddings = dict()
        for filename in filenames:
            embeddings[filename] = self.embed_single_file(filename)
        return embeddings

    def export(self, filename):
        with open(filename, 'w') as file:
            for key, value in self._embeddings.items():
                file.write(f'{key},{value}\n')

    def __iter__(self):
        for key, value in self._embeddings.items():
            yield key, value

    def __repr__(self):
        return f'fileEmbedder(model={self._model_name})'
