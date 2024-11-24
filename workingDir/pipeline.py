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

from collections import Counter
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import ssl

# Download NLTK data
import nltk
ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
#By Vihaan Nama
#Some parts of code and documentation generated using AI - Claude, Perplexity, ChatGPT



def create_text(directory, output_directory_name, output_normal_directory_name):
    """
    Processes PDF files from the './data' directory and extracts their text content.
    
    This function:
    1. Reads all PDF files in the './data' directory
    2. Extracts text from each page
    3. Cleans the extracted text by removing hidden characters
    4. Saves both cleaned and original versions to separate output directories

    Args: 
    directory - Directory where the original PDF files are present in.
    output_directory_name - Directory where the processed output of the PDF documents should be sent.
    output_normal_directory_name - Directory where the unprocessed output of the PDF documents should be written.
    
    Output files are saved in:
    - './output/' for cleaned text
    - './output_normal/' for original text
    """
    c = ''
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            print(filename)
            c = filename[:-4]
        # Open the PDF file
        with pdfplumber.open(directory + "/" + filename) as pdf:

            # Iterate through all pages
            
            text = ''
            pages = pdf.pages
            text_total = ''
            total_text_normal = ''
            for page in pages:
                # Extract text from the page
                text = page.extract_text()
                
                text_normal = text
                # Remove common hidden characters, but keep newlines
                text = re.sub(r'[\x00-\x09\x0B-\x1F\x7F-\x9F]', '', text)
            
                # Remove zero-width characters
                text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)
            
                # Remove other invisible separator characters, but keep newlines
                text = re.sub(r'[\u2000-\u200F\u2028-\u202E\u205F-\u206F]', '', text)
            
                # Remove control characters, but keep newlines
                text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')

                text = re.sub(r'\n', ' ', text)
            
                text_total += text 
                total_text_normal += text_normal
            
            # write total text without any line seperation to the output directory - modified
            with open(output_directory_name +'/output' + str(c) + '.txt', 'w') as file:      
                file.write(text_total)
            
            # write total text - normal without modification to the output_normal directory
            with open(output_normal_directory_name + '/output_normal' + str(c) + '.txt', 'w') as file:      
                file.write(total_text_normal)

def write_chunks_to_file(chunks, output_file, separator="\n---\n"):
    """
    Writes text chunks to a file with a separator between them.
    
    Args:
        chunks (list): List of text chunks to write
        output_file (str): Path to the output file
        separator (str, optional): String to use as separator between chunks. Defaults to "\n---\n"

    Output:
        
    """
    with open(output_file, 'w') as file:
        for i, chunk in enumerate(chunks):
            file.write(chunk)
            if i < len(chunks) - 1:
                file.write(separator)

def create_chunks(output_directory_name, recursive_directory_name, semantic_directory_name, tokenwise_directory_name):
    """
    Creates different types of text chunks from processed PDF text files.
    
    This function:
    1. Loads OpenAI API key from environment variables
    2. Processes text files from the './output' directory
    3. Creates three different types of chunks using:
       - RecursiveCharacterTextSplitter (1000 chars, 200 overlaps)
       - TokenTextSplitter (100 tokens, 20 overlap)
       - SemanticChunker (using OpenAI embeddings)

    Args:
    output_directory_name - Directory where the processed output of the PDF documents should be sent.
    recursive_directory_name - Directory where the Recursive text file outputs of the text files should be written.
    semantic_directory_name - Directory where the Semantic text file outputs of the text files should be written.
    tokenwise_directory_name - Directory where the TokenWise text file outputs of the text files should be written.
    
    Output files are saved in:
    - '../Recursive/' for recursive character splits
    - '../TokenWise/' for token-based splits
    - '../Semantic/' for semantic-based splits
    """

    load_dotenv()  # This loads the variables from .env
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key #initialise openAI api key
    directory = output_directory_name
    c = ''
    # Got through the output directory and perform chunking on each text file present
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            print(filename)
            c = filename[6:-4]
        with open(directory + '/' + filename, 'r', encoding='utf-8') as file:
            # Read the entire contents of the file
            text = file.read()

        #Start of Recursive Chunking Process
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_text(text)
        write_chunks_to_file(chunks=chunks, output_file=recursive_directory_name +'/Recursive-Chunker-' + str(c) + '.txt')

        
        #Start of Tokenwise Chunking Process
        text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
        chunks = text_splitter.split_text(text)
        write_chunks_to_file(chunks=chunks, output_file=tokenwise_directory_name + '/Token-Chunker-' + str(c) + '.txt')
        
        #Start of Semantic Chunking Process
        text_splitter = SemanticChunker(OpenAIEmbeddings())
        # Split the text into chunks
        chunks = text_splitter.split_text(text)
        write_chunks_to_file(chunks=chunks, output_file=semantic_directory_name + '/Semantic-Chunker-' + str(c) + '.txt')

def extract_metadata(input_folder, output_folder):
    """
    Creates metadata text from processed PDF text files.
    
    This function:
    1. Processes text files from the './output' directory
    2. Creates metadata of each PDF file

    Args:
    input_folder - Directory where the processed output of the PDF documents should be sent.
    output_folder - Directory where the metadata text file outputs of the text files should be written.
   
    Output files are saved in:
    - '../metadata/' for recursive character splits
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    c = ''
    for filename in os.listdir(input_folder):
        c = filename[6:-4]
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"metadata{c}.txt")

            with open(input_path, 'r') as input_file:
                content = input_file.read()

            pattern = r'(.*?)(J U D G M E N T|JUDGMENT|O R D E R|ORDER)'
            match = re.search(pattern, content, re.DOTALL)

            if match:
                metadata = match.group(1).strip()
                with open(output_path, 'w') as output_file:
                    output_file.write(metadata)

def read_chunks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    chunks = re.split(r'---', content)
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def get_all_chunks(folder_path):
    all_chunks = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            all_chunks.extend(read_chunks(file_path))
    return all_chunks

def tokenize_and_clean(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    return tokens

def recursive_eda(directory):
    folder_path = directory
    all_chunks = get_all_chunks(folder_path)
    all_tokens = [tokenize_and_clean(chunk) for chunk in all_chunks]

    # 1. Average chunk size (in characters)
    avg_chunk_size = np.mean([len(chunk) for chunk in all_chunks])
    print(f"1. Average chunk size: {avg_chunk_size:.2f} characters")

    # 2. Average words per chunk
    avg_words_per_chunk = np.mean([len(tokens) for tokens in all_tokens])
    print(f"2. Average words per chunk: {avg_words_per_chunk:.2f}")

    # 3. Most occurring words
    all_words = [word for tokens in all_tokens for word in tokens]
    word_freq = Counter(all_words)
    print("3. Top 10 most occurring words:")
    for word, count in word_freq.most_common(10):
        print(f"   {word}: {count}")

    # 4. Unique words count
    unique_words = set(all_words)
    print(f"4. Total unique words: {len(unique_words)}")

    # 5. Average word length
    avg_word_length = np.mean([len(word) for word in all_words])
    print(f"5. Average word length: {avg_word_length:.2f} characters")

    # 6. Chunk length distribution
    chunk_lengths = [len(chunk) for chunk in all_chunks]
    print(f"6. Chunk length distribution:")
    print(f"   Min: {min(chunk_lengths)}")
    print(f"   Max: {max(chunk_lengths)}")
    print(f"   Median: {np.median(chunk_lengths):.2f}")
    print(f"   Standard deviation: {np.std(chunk_lengths):.2f}")

    # 7. Word count distribution
    word_counts = [len(tokens) for tokens in all_tokens]
    print(f"7. Word count distribution:")
    print(f"   Min: {min(word_counts)}")
    print(f"   Max: {max(word_counts)}")
    print(f"   Median: {np.median(word_counts):.2f}")
    print(f"   Standard deviation: {np.std(word_counts):.2f}")

    # 8. Percentage of chunks with numbers
    chunks_with_numbers = sum(1 for chunk in all_chunks if any(char.isdigit() for char in chunk))
    percentage_chunks_with_numbers = (chunks_with_numbers / len(all_chunks)) * 100
    print(f"8. Percentage of chunks with numbers: {percentage_chunks_with_numbers:.2f}%")

    # 9. Average sentence count per chunk
    def count_sentences(text):
        return len(re.findall(r'\w+[.!?][\s$]', text, re.MULTILINE))

    avg_sentences_per_chunk = np.mean([count_sentences(chunk) for chunk in all_chunks])
    print(f"9. Average sentences per chunk: {avg_sentences_per_chunk:.2f}")

    # 10. Token frequency distribution
    token_freq = Counter(all_words)
    print("10. Token frequency distribution:")
    print(f"   Tokens appearing only once: {sum(1 for count in token_freq.values() if count == 1)}")
    print(f"   Tokens appearing 2-5 times: {sum(1 for count in token_freq.values() if 2 <= count <= 5)}")
    print(f"   Tokens appearing 6-10 times: {sum(1 for count in token_freq.values() if 6 <= count <= 10)}")
    print(f"   Tokens appearing more than 10 times: {sum(1 for count in token_freq.values() if count > 10)}")

def semantic_eda(directory):
    folder_path = directory
    all_chunks = get_all_chunks(folder_path)
    all_tokens = [tokenize_and_clean(chunk) for chunk in all_chunks]

    # 1. Average chunk size (in characters)
    avg_chunk_size = np.mean([len(chunk) for chunk in all_chunks])
    print(f"1. Average chunk size: {avg_chunk_size:.2f} characters")

    # 2. Average words per chunk
    avg_words_per_chunk = np.mean([len(tokens) for tokens in all_tokens])
    print(f"2. Average words per chunk: {avg_words_per_chunk:.2f}")

    # 3. Most occurring words
    all_words = [word for tokens in all_tokens for word in tokens]
    word_freq = Counter(all_words)
    print("3. Top 10 most occurring words:")
    for word, count in word_freq.most_common(10):
        print(f"   {word}: {count}")

    # 4. Unique words count
    unique_words = set(all_words)
    print(f"4. Total unique words: {len(unique_words)}")

    # 5. Average word length
    avg_word_length = np.mean([len(word) for word in all_words])
    print(f"5. Average word length: {avg_word_length:.2f} characters")

    # 6. Chunk length distribution
    chunk_lengths = [len(chunk) for chunk in all_chunks]
    print(f"6. Chunk length distribution:")
    print(f"   Min: {min(chunk_lengths)}")
    print(f"   Max: {max(chunk_lengths)}")
    print(f"   Median: {np.median(chunk_lengths):.2f}")
    print(f"   Standard deviation: {np.std(chunk_lengths):.2f}")

    # 7. Word count distribution
    word_counts = [len(tokens) for tokens in all_tokens]
    print(f"7. Word count distribution:")
    print(f"   Min: {min(word_counts)}")
    print(f"   Max: {max(word_counts)}")
    print(f"   Median: {np.median(word_counts):.2f}")
    print(f"   Standard deviation: {np.std(word_counts):.2f}")

    # 8. Percentage of chunks with numbers
    chunks_with_numbers = sum(1 for chunk in all_chunks if any(char.isdigit() for char in chunk))
    percentage_chunks_with_numbers = (chunks_with_numbers / len(all_chunks)) * 100
    print(f"8. Percentage of chunks with numbers: {percentage_chunks_with_numbers:.2f}%")

    # 9. Average sentence count per chunk
    def count_sentences(text):
        return len(re.findall(r'\w+[.!?][\s$]', text, re.MULTILINE))

    avg_sentences_per_chunk = np.mean([count_sentences(chunk) for chunk in all_chunks])
    print(f"9. Average sentences per chunk: {avg_sentences_per_chunk:.2f}")

    # 10. Token frequency distribution
    token_freq = Counter(all_words)
    print("10. Token frequency distribution:")
    print(f"   Tokens appearing only once: {sum(1 for count in token_freq.values() if count == 1)}")
    print(f"   Tokens appearing 2-5 times: {sum(1 for count in token_freq.values() if 2 <= count <= 5)}")
    print(f"   Tokens appearing 6-10 times: {sum(1 for count in token_freq.values() if 6 <= count <= 10)}")
    print(f"   Tokens appearing more than 10 times: {sum(1 for count in token_freq.values() if count > 10)}")

def tokenwise_eda(directory):
    folder_path = directory
    all_chunks = get_all_chunks(folder_path)
    all_tokens = [tokenize_and_clean(chunk) for chunk in all_chunks]

    # 1. Average chunk size (in characters)
    avg_chunk_size = np.mean([len(chunk) for chunk in all_chunks])
    print(f"1. Average chunk size: {avg_chunk_size:.2f} characters")

    # 2. Average words per chunk
    avg_words_per_chunk = np.mean([len(tokens) for tokens in all_tokens])
    print(f"2. Average words per chunk: {avg_words_per_chunk:.2f}")

    # 3. Most occurring words
    all_words = [word for tokens in all_tokens for word in tokens]
    word_freq = Counter(all_words)
    print("3. Top 10 most occurring words:")
    for word, count in word_freq.most_common(10):
        print(f"   {word}: {count}")

    # 4. Unique words count
    unique_words = set(all_words)
    print(f"4. Total unique words: {len(unique_words)}")

    # 5. Average word length
    avg_word_length = np.mean([len(word) for word in all_words])
    print(f"5. Average word length: {avg_word_length:.2f} characters")

    # 6. Chunk length distribution
    chunk_lengths = [len(chunk) for chunk in all_chunks]
    print(f"6. Chunk length distribution:")
    print(f"   Min: {min(chunk_lengths)}")
    print(f"   Max: {max(chunk_lengths)}")
    print(f"   Median: {np.median(chunk_lengths):.2f}")
    print(f"   Standard deviation: {np.std(chunk_lengths):.2f}")

    # 7. Word count distribution
    word_counts = [len(tokens) for tokens in all_tokens]
    print(f"7. Word count distribution:")
    print(f"   Min: {min(word_counts)}")
    print(f"   Max: {max(word_counts)}")
    print(f"   Median: {np.median(word_counts):.2f}")
    print(f"   Standard deviation: {np.std(word_counts):.2f}")

    # 8. Percentage of chunks with numbers
    chunks_with_numbers = sum(1 for chunk in all_chunks if any(char.isdigit() for char in chunk))
    percentage_chunks_with_numbers = (chunks_with_numbers / len(all_chunks)) * 100
    print(f"8. Percentage of chunks with numbers: {percentage_chunks_with_numbers:.2f}%")

    # 9. Average sentence count per chunk
    def count_sentences(text):
        return len(re.findall(r'\w+[.!?][\s$]', text, re.MULTILINE))

    avg_sentences_per_chunk = np.mean([count_sentences(chunk) for chunk in all_chunks])
    print(f"9. Average sentences per chunk: {avg_sentences_per_chunk:.2f}")

    # 10. Token frequency distribution
    token_freq = Counter(all_words)
    print("10. Token frequency distribution:")
    print(f"   Tokens appearing only once: {sum(1 for count in token_freq.values() if count == 1)}")
    print(f"   Tokens appearing 2-5 times: {sum(1 for count in token_freq.values() if 2 <= count <= 5)}")
    print(f"   Tokens appearing 6-10 times: {sum(1 for count in token_freq.values() if 6 <= count <= 10)}")
    print(f"   Tokens appearing more than 10 times: {sum(1 for count in token_freq.values() if count > 10)}")



def main():
    """
    Main function that orchestrates the PDF processing and chunking pipeline.
    
    This function:
    1. Calls create_text() to process PDFs and extract text
    2. Calls create_chunks() to generate different types of text chunks
    """

    
    print("\n\n\n\n")
    print("------- Extracting Text From PDFs -------")
    directory_name = '../data'
    output_directory_name = '../output'
    output_normal_directory_name = '../output_normal'
    create_text(directory_name, output_directory_name, output_normal_directory_name)
    print("------- Extracting Text From PDFs Done -------")
    print("\n\n\n\n")

    print("------- Extracting Metadata -------")
    input_folder = '../output'
    output_folder = '../metadata'
    extract_metadata(input_folder, output_folder)
    print("------- Extracting Metadata Done -------")
    print("\n\n\n\n")

    print("------- Chunking -------")
    recursive_directory_name = '../Recursive'
    semantic_directory_name = '../Semantic'
    tokenwise_directory_name = '../TokenWise'
    create_chunks(output_directory_name, recursive_directory_name, semantic_directory_name, tokenwise_directory_name)
    print("------- Chunking Done -------")
    print("\n\n\n\n")
    
    print("------- Recursive EDA -------")
    recursive_eda(recursive_directory_name)
    print("------- Recursive EDA Done -------")
    print("\n\n\n\n")

    print("------- Semantic EDA -------")
    semantic_eda(semantic_directory_name)
    print("------- Semantic EDA Done -------")
    print("\n\n\n\n")

    print("------- TokenWise EDA -------")
    tokenwise_eda(tokenwise_directory_name)
    print("------- TokenWise EDA Done -------")

if __name__ == "__main__":
    main()
    
