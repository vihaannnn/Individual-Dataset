import os
import re
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

folder_path = 'TokenWise'
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