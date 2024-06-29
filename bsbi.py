from collections import defaultdict
from tqdm import tqdm

class BSBI_Block:

    def __init__(self, vocabulary: dict, block: list[str], output: str, encoding: str = "utf8"):
        self.vocabulary = vocabulary
        self.block = block
        self.output = output
        self.encoding = encoding

    def construct_index(self):
        index = defaultdict(list)

        print("Starting constructing index")
        for file in tqdm(self.block):
            with open(file, 'r', encoding=self.encoding) as f:
                doc_id = int(file.split("/")[-1][2:].split("_")[0])
                for term in f:
                    term = term.strip()
                    if not term:
                        continue
                    if term in self.vocabulary:
                        if doc_id  not in index[self.vocabulary[term]]:
                            index[self.vocabulary[term]].append(doc_id)
                    else:
                        self.vocabulary[term] = len(self.vocabulary)
                        if doc_id  not in index[self.vocabulary[term]]:
                            index[self.vocabulary[term]].append(doc_id)
        
        with open(self.output, "w", encoding=self.encoding) as f:
            for key in sorted(index):
                f.write(f"{key} {index[key]}\n")

def merge(block_outs: list[str], vocabulary: dict, output: str, encoding: str = "utf8"):
    vocabulary = {v: k for k, v in vocabulary.items()}
    output = open(output, "w", encoding=encoding)
    streams = {stream: stream.__next__() for stream in [open(file, "r", encoding=encoding) for file in block_outs]}
    while streams:
        cur_id = None
        docs = []
        for s in sorted(streams, key=lambda x: int(streams[x].split(" ")[0])):
            try:
                line = streams[s].strip()
                token = int(line.split(" ")[0])
                if not cur_id:
                    cur_id = token
                if cur_id == token:
                    docs += eval(line[len(str(token)):])
                    streams[s] = s.__next__()
                else:
                    break
            except:
                s.close()
                streams.pop(s)
        output.write(f"{vocabulary[cur_id]} {docs}\n")
    output.close()
        
