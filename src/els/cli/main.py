import argparse
from els.embed.generate import fileEmbedder
from els.utils.files import filer
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Embed files into vector database")
    parser.add_argument('files', nargs='+', type=str, help='File to embed')

    args = parser.parse_args()
    files = args.files

    F = filer()
    for file in files:
        F.enroll(os.path.abspath(file))
    
    export = F.export()
    E = fileEmbedder()
    embeddings = dict()
    for mimetype, files in export['text'].items():
        for hash, filePath in files.items():
            embeddings[hash] = E.embed_single_file(filePath)

    for mimetyoe, files in export['binary'].items():
        print(files)
    print(embeddings)


