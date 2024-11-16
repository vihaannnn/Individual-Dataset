from langchain.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
import os

load_dotenv()  # This loads the variables from .env
api_key = os.getenv("OPENAI_API_KEY")
import openai

openai.api_key = api_key

def write_chunks_to_file(chunks, output_file, separator="\n---\n"):
    with open(output_file, 'w') as file:
        for i, chunk in enumerate(chunks):
            file.write(chunk)
            if i < len(chunks) - 1:
                file.write(separator)

import os

directory = './output'
c = 1
for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        print(filename)
    with open('./output/' + filename, 'r', encoding='utf-8') as file:
        # Read the entire contents of the file
        text = file.read()


    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_text(text)

    # for chunk in chunks:
    #     print(chunk)
    #     print("*************************************")

    write_chunks_to_file(chunks=chunks, output_file='./Recursive/Recusrive-Chunker-' + str(c) + '.txt')

    from langchain.text_splitter import TokenTextSplitter

    text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
    chunks = text_splitter.split_text(text)

    write_chunks_to_file(chunks=chunks, output_file='./TokenWise/Token-Chunker-' + str(c) + '.txt')


    from langchain_experimental.text_splitter import SemanticChunker
    from langchain_openai.embeddings import OpenAIEmbeddings

    text_splitter = SemanticChunker(OpenAIEmbeddings())



    # Split the text into chunks
    chunks = text_splitter.split_text(text)

    write_chunks_to_file(chunks=chunks, output_file='./Semantic/Semantic-Chunker-' + str(c) + '.txt')


    # from langchain_experimental.text_splitter import SemanticChunker

    # semantic_splitter = SemanticChunker(chunk_size=1000, chunk_overlap=200)
    # chunks = semantic_splitter.split_text(text)

    c += 1