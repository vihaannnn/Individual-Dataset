import os
import re

def extract_metadata(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"metadata_{filename}.txt")

            with open(input_path, 'r') as input_file:
                content = input_file.read()

            pattern = r'(.*?)(J U D G M E N T|JUDGMENT|O R D E R|ORDER)'
            match = re.search(pattern, content, re.DOTALL)

            if match:
                metadata = match.group(1).strip()
                with open(output_path, 'w') as output_file:
                    output_file.write(metadata)

# Usage
input_folder = 'output'
output_folder = 'metadata'
extract_metadata(input_folder, output_folder)