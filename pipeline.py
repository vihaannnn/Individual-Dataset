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
#By Vihaan Nama
#Some parts of code and documentation generated using AI - Claude, Perplexity, ChatGPT

def paragraph_chunking(text, paragraphs_per_chunk):
    """
    Splits text into chunks based on paragraphs.
    
    Args:
        text (str): The input text to be chunked
        paragraphs_per_chunk (int): Number of paragraphs to include in each chunk
    
    Returns:
        list: A list of text chunks, where each chunk contains the specified number of paragraphs
    """
    paragraphs = text.split('\n\n')
    return ['\n\n'.join(paragraphs[i:i+paragraphs_per_chunk]) for i in range(0, len(paragraphs), paragraphs_per_chunk)]

def write_array_to_file(array, filename, lines_between):
    """
    Writes an array of strings to a file with specified number of empty lines between entries.
    
    Args:
        array (list): List of strings to write to file
        filename (str): Path to the output file
        lines_between (int): Number of empty lines to insert between array items
    """
    with open(filename, 'w', newline='') as file:
        for i, item in enumerate(array):
            file.write(item + os.linesep)
            if i < len(array) - 1:  # Don't add extra lines after the last item
                file.write(os.linesep * lines_between)

def remove_newlines(string_array):
    """
    Removes leading and trailing whitespace from each string in an array.
    
    Args:
        string_array (list): List of strings to process
    
    Returns:
        list: List of strings with whitespace removed
    """
    return [s.strip() for s in string_array]

def create_text():
    """
    Processes PDF files from the './data' directory and extracts their text content.
    
    This function:
    1. Reads all PDF files in the './data' directory
    2. Extracts text from each page
    3. Cleans the extracted text by removing hidden characters
    4. Saves both cleaned and original versions to separate output directories
    
    Output files are saved in:
    - './output/' for cleaned text
    - './output_normal/' for original text
    """
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
    """
    Writes text chunks to a file with a separator between them.
    
    Args:
        chunks (list): List of text chunks to write
        output_file (str): Path to the output file
        separator (str, optional): String to use as separator between chunks. Defaults to "\n---\n"
    """
    with open(output_file, 'w') as file:
        for i, chunk in enumerate(chunks):
            file.write(chunk)
            if i < len(chunks) - 1:
                file.write(separator)

def create_chunks():
    """
    Creates different types of text chunks from processed PDF text files.
    
    This function:
    1. Loads OpenAI API key from environment variables
    2. Processes text files from the './output' directory
    3. Creates three different types of chunks using:
       - RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
       - TokenTextSplitter (100 tokens, 20 overlap)
       - SemanticChunker (using OpenAI embeddings)
    
    Output files are saved in:
    - './Recursive/' for recursive character splits
    - './TokenWise/' for token-based splits
    - './Semantic/' for semantic-based splits
    """

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
    """
    Main function that orchestrates the PDF processing and chunking pipeline.
    
    This function:
    1. Calls create_text() to process PDFs and extract text
    2. Calls create_chunks() to generate different types of text chunks
    """
    create_text()
    create_chunks()

if __name__ == "__main__":
    main()