from workingDir.pipeline import create_text, create_chunks, extract_metadata
import pytest
import os

def test_create_text():
    directory_name = 'test/test-data'
    output_directory_name = 'test/test-output'
    output_normal_directory_name = 'test/test-output_normal'
    assert os.path.exists('test/test-data/1000.pdf'), "Input Not Present"

    create_text(directory_name, output_directory_name, output_normal_directory_name)
    assert os.path.exists('test/test-output/output1000.txt'), "Output not generated"
    assert os.path.exists('test/test-output_normal/output_normal1000.txt'), "Normal Output not generated"
    
    
def test_create_chunks():
    recursive_directory_name = 'test/test-Recursive'
    semantic_directory_name = 'test/test-Semantic'
    tokenwise_directory_name = 'test/test-TokenWise'
    output_directory_name = 'test/test-output'

    assert os.path.exists('test/test-output/output1000.txt'), "Output not present"

    create_chunks(output_directory_name, recursive_directory_name, semantic_directory_name, tokenwise_directory_name)

    assert os.path.exists('test/test-Recursive/Recursive-Chunker-1000.txt'), "Recursive Chunks not generated"
    assert os.path.exists('test/test-Semantic/Semantic-Chunker-1000.txt'), "Semantic Chunks not generated"
    assert os.path.exists('test/test-Tokenwise/Token-Chunker-1000.txt'), "TokenWise Chunks not generated"

def test_extract_metadata():
    input_directory = 'test/test-output'
    output_directory = 'test/test-metadata'

    extract_metadata(input_folder=input_directory, output_folder=output_directory)

    assert os.path.exists('test/test-metadata/metadata1000.txt')
