from els.utils.mimetype import is_binary
import pathlib
import hashlib
import mimetypes

class filer:
    def __init__(self):
        self.files = dict()
    
    def enroll(self, filePath):
        with open(filePath, 'rb') as f:
            fileHash = hashlib.md5(f.read()).hexdigest()
        if not fileHash in self.files:
            self.files[fileHash] = filePath

    def get(self, fileHash):
        return self.files[fileHash]

    def list_files(self):
        return self.files

    def export(self):
        out = {'text': {}, 'binary': {}}
        for fileHash, filePath in self.files.items():
            mime, _ = mimetypes.guess_type(filePath)
            if is_binary(filePath):
                if out['binary'].get(mime, ...) == ...:
                    out['binary'][mime] = {}
                out['binary'][mime][fileHash] = filePath
            else:
                if out['text'].get(mime, ...) == ...:
                    out['text'][mime] = {}
                out['text'][mime][fileHash] = filePath
        return out

    def __repr__(self):
        return f"filer: {self.files}"


def index_directory(root, recursive=False):
    f = filer()
    if recursive:
        for p in pathlib.Path(root).rglob('*'):
            if p.is_file():
                f.enroll(p)
    else:
        for p in pathlib.Path(root).iterdir():
            if p.is_file():
                f.enroll(p)
    return f

