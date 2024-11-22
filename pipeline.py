import pdfplumber
import os
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import openai
from langchain.text_splitter import TokenTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings


def paragraph_chunking(text, paragraphs_per_chunk):
    paragraphs = text.split('\n\n')
    return ['\n\n'.join(paragraphs[i:i+paragraphs_per_chunk]) for i in range(0, len(paragraphs), paragraphs_per_chunk)]

def write_array_to_file(array, filename, lines_between):
    with open(filename, 'w', newline='') as file:
        for i, item in enumerate(array):
            file.write(item + os.linesep)
            if i < len(array) - 1:  # Don't add extra lines after the last item
                file.write(os.linesep * lines_between)

def remove_newlines(string_array):
    return [s.strip() for s in string_array]

def create_text():
    directory = './data'
    c = ''
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            print(filename)
            c = filename[:-4]
        # Open the PDF file
        with pdfplumber.open("./data/" + filename) as pdf:

            # Iterate through all pages
            

            text = ''
            pages = pdf.pages
            text_total = ''
            total_text_normal = ''
            for page in pages:
                # print(type(pdf.pages))
                # Extract text from the page
                text = page.extract_text()
                
                text_normal = text
                # print(text)
                # Remove common hidden characters, but keep newlines
                text = re.sub(r'[\x00-\x09\x0B-\x1F\x7F-\x9F]', '', text)
            
                # Remove zero-width characters
                text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)
            
                # Remove other invisible separator characters, but keep newlines
                text = re.sub(r'[\u2000-\u200F\u2028-\u202E\u205F-\u206F]', '', text)
            
                # Remove control characters, but keep newlines
                text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')

                text = re.sub(r'\n', ' ', text)
            
                # Normalize whitespace (optional)
                # text = ' '.join(text.split())
                text_total += text 
                total_text_normal += text_normal
            
            with open('./output/output' + str(c) + '.txt', 'w') as file:      
                file.write(text_total)
            
            with open('./output_normal/output_normal' + str(c) + '.txt', 'w') as file:      
                file.write(total_text_normal)

def write_chunks_to_file(chunks, output_file, separator="\n---\n"):
    with open(output_file, 'w') as file:
        for i, chunk in enumerate(chunks):
            file.write(chunk)
            if i < len(chunks) - 1:
                file.write(separator)

def create_chunks():
    load_dotenv()  # This loads the variables from .env
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    directory = './output'
    c = ''
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            print(filename)
            c = filename[6:-4]
        with open('./output/' + filename, 'r', encoding='utf-8') as file:
            # Read the entire contents of the file
            text = file.read()


        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = text_splitter.split_text(text)
        write_chunks_to_file(chunks=chunks, output_file='./Recursive/Recusrive-Chunker-' + str(c) + '.txt')

        

        text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
        chunks = text_splitter.split_text(text)
        write_chunks_to_file(chunks=chunks, output_file='./TokenWise/Token-Chunker-' + str(c) + '.txt')
        
        
        
        text_splitter = SemanticChunker(OpenAIEmbeddings())

        # Split the text into chunks
        chunks = text_splitter.split_text(text)

        write_chunks_to_file(chunks=chunks, output_file='./Semantic/Semantic-Chunker-' + str(c) + '.txt')


def main():
    create_text()

if __name__ == "__main__":
    main()