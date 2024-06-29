import os

from bsbi import BSBI_Block, merge
from multiprocessing import Process

MAX_SIZE = 4294967296

if __name__ == "__main__":
    files = ["data/" + file for file in os.listdir("data")]

    blocks = [[]]
    cur_size = 0
    for file in files:
        file_size = os.stat(file).st_size
        if cur_size + file_size > MAX_SIZE:
            cur_size = file_size
            blocks.append([file])
        else:
            cur_size += file_size
            blocks[-1].append(file)

    print(f"Blocks: {len(blocks)}")
    
    vocabulary = dict()

    for i, block in enumerate(blocks):
        bsbi = BSBI_Block(vocabulary, block, f"temp/block_output_{i}.txt")
        bsbi.construct_index()
        del bsbi

    # proc = []
    # for i, block in enumerate(blocks):
    #     bsbi = BSBI_Block(vocabulary, block, f"temp/block_output_{i}.txt")
    #     p = Process(target=bsbi.construct_index)
    #     p.start()
    #     proc.append(p)
    # for p in proc:
    #     p.join()

    merge(["temp/" + file for file in os.listdir("temp")], vocabulary, "index.txt")