from sentence_transformers import SentenceTransformer

class fileEmbedder:
    def __init__(self, model='all-MiniLM-L6-v2'):
        self._model = SentenceTransformer(model)
        self._model_name = model
        self._embeddings = dict()

    def embed_single_string(self, string, stringName):
        self._embeddings[stringName] = self._model.encode(string)

    def embed_single_file(self, filename):
        with open(filename, 'r') as file:
            self.embed_single_string(file.read(), filename)

    def embed_multiple_files(self, filenames):
        for filename in filenames:
            self.embed_single_file(filename)

    def __repr__(self):
        return f'fileEmbedder(model={self._model_name})'
