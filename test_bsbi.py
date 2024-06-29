import pytest
from bsbi import BSBI_Block, merge

vocabulary = {
    "and": 1,
    "antihor": 2,
    "by": 3,
    "goodby": 4,
    "hello": 5,
    "hurey": 6,
    "ihor": 7, 
    "woo": 8,
    "world": 9,
    "how": 10,
    "are": 11,
    "you": 12
}

def test_BSBI_block():
    blocks = [["test-data/raw-data/TS1_tokens.txt", "test-data/raw-data/TS2_tokens.txt"], ["test-data/raw-data/TS3_tokens.txt"]]
    for i, block in enumerate(blocks):
        bsbi = BSBI_Block(vocabulary, block, f"test-data/temp/block_output_{i}.txt")
        bsbi.construct_index()
    
    for i in range(2):
        str_out = open(f"test-data/temp/block_output_{i}.txt", "r").read()
        str_test = open(f"test-data/temp/test_block_output_{i}.txt", "r").read()
        assert str_out == str_test

def test_merge():
    merge(["test-data/temp/test_block_output_0.txt", "test-data/temp/test_block_output_1.txt"], vocabulary, "test-data/index.txt")
    str_out = open("test-data/index.txt", "r").read()
    str_test = open("test-data/test_index.txt", "r").read()
    assert str_out == str_test