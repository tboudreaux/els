import PyPDF2

class pdf:
    def __init__(self, filePath):
        self.path = filePath

    def get_text(self):
        with open(self.path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            text = ''
            for page in range(reader.numPages):
                text += reader.getPage(page).extract_text()
        return text

    def __repr__(self):
        return f'(PDF: {self.path})'


