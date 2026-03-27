import PyPDF2
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    
    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    words = text.split()
    
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words]
    
    return " ".join(words)