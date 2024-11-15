from langchain.text_splitter import RecursiveCharacterTextSplitter

def write_chunks_to_file(chunks, output_file, separator="\n---\n"):
    with open(output_file, 'w') as file:
        for i, chunk in enumerate(chunks):
            file.write(chunk)
            if i < len(chunks) - 1:
                file.write(separator)


with open('./RawFiles/output1.txt', 'r', encoding='utf-8') as file:
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

write_chunks_to_file(chunks=chunks, output_file="./Recursive/Recusrive-Chunker-1.txt")

from langchain.text_splitter import TokenTextSplitter

text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = text_splitter.split_text(text)

write_chunks_to_file(chunks=chunks, output_file="./TokenWise/Token-Chunker-1.txt")