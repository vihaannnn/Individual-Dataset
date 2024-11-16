import pdfplumber
import os
import re


def paragraph_chunking(text, paragraphs_per_chunk):
    paragraphs = text.split('\n\n')
    return ['\n\n'.join(paragraphs[i:i+paragraphs_per_chunk]) for i in range(0, len(paragraphs), paragraphs_per_chunk)]

# def write_array_to_file(array, filename, lines_between):
#     with open(filename, 'w') as file:
#         for i, item in enumerate(array):
#             file.write(item)
#             if i < len(array) - 1:  # Don't add extra lines after the last item
#                 file.write('\n' * (lines_between + 1))



def write_array_to_file(array, filename, lines_between):
    with open(filename, 'w', newline='') as file:
        for i, item in enumerate(array):
            file.write(item + os.linesep)
            if i < len(array) - 1:  # Don't add extra lines after the last item
                file.write(os.linesep * lines_between)



def remove_newlines(string_array):
    return [s.strip() for s in string_array]

import os

directory = './data'

for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        print(filename)    
    # Open the PDF file
    with pdfplumber.open("data/1.pdf") as pdf:

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
        
        with open('output1.txt', 'w') as file:      
            file.write(text_total)
        
        with open('output_normal1.txt', 'w') as file:      
            file.write(total_text_normal)

        print(type(text_total))
        chunks = paragraph_chunking(text_total, 2)
        chunks = remove_newlines(chunks)
        write_array_to_file(chunks, '1.txt', lines_between=4)
        # print(chunks)