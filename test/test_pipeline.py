from workingDir.pipeline import create_text, create_chunks, extract_metadata, recursive_eda, semantic_eda, tokenwise_eda
import pytest
import os

def test_create_text():
    """
    Tests the `create_text` function to ensure it processes PDF files correctly.

    This test:
    1. Verifies the presence of an input file in the specified directory.
    2. Calls the `create_text` function with test input and output directories.
    3. Asserts the existence of generated output files (processed and unprocessed).

    Raises:
        AssertionError: If the input file is missing or the output files are not generated.
    """
    directory_name = 'test/test-data'
    output_directory_name = 'test/test-output'
    output_normal_directory_name = 'test/test-output_normal'
    assert os.path.exists('test/test-data/1000.pdf'), "Input Not Present"

    create_text(directory_name, output_directory_name, output_normal_directory_name)
    assert os.path.exists('test/test-output/output1000.txt'), "Output not generated"
    assert os.path.exists('test/test-output_normal/output_normal1000.txt'), "Normal Output not generated"
    
    
def test_create_chunks():
    """
    Tests the `create_chunks` function to ensure text chunking is performed correctly.

    This test:
    1. Verifies the presence of a processed text file in the specified output directory.
    2. Calls the `create_chunks` function with test directories for chunk outputs.
    3. Asserts the existence of output files for recursive, semantic, and token-wise chunking.

    Raises:
        AssertionError: If the input file is missing or the chunk output files are not generated.
    """
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
    """
    Tests the `extract_metadata` function to ensure metadata extraction is accurate.

    This test:
    1. Calls the `extract_metadata` function with test input and output directories.
    2. Asserts the existence of the metadata file generated in the output directory.

    Raises:
        AssertionError: If the metadata output file is not generated.
    """
    input_directory = 'test/test-output'
    output_directory = 'test/test-metadata'

    extract_metadata(input_folder=input_directory, output_folder=output_directory)

    assert os.path.exists('test/test-metadata/metadata1000.txt'), "Metadata Not Extracted"

def test_eda():
    """
    Tests the exploratory data analysis (EDA) functions for chunked text files.

    This test:
    1. Verifies the presence of processed text files.
    2. Calls the `recursive_eda`, `semantic_eda`, and `tokenwise_eda` functions with respective directories.
    
    Note:
        This test does not assert outputs directly but ensures the EDA functions execute without errors.
    
    Raises:
        AssertionError: If the required input files are not present.
    """
    assert os.path.exists('test/test-output/output1000.txt'), "Output not present"
    recursive_directory_name = 'test/test-Recursive'
    semantic_directory_name = 'test/test-Semantic'
    tokenwise_directory_name = 'test/test-TokenWise'
    recursive_eda(recursive_directory_name)
    semantic_eda(semantic_directory_name)
    tokenwise_eda(tokenwise_directory_name)
