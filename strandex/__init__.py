import os.path
import re
import sys
import argparse
import random
from six.moves import range

__version__ = "0.3"

class FastqSampler:
    pattern = re.compile(r'@.+[\n\r]+.+[\n\r]+\+.*?[\n\r].+[\n\r]')

    def __init__(self, fastq1, fastq2=None, nreads=1, seed=None):
        random.seed(seed)
        self.fastq1 = open(fastq1, "r")
        self.fastq1_size = os.path.getsize(fastq1)
        if fastq2 is not None:
            self.fastq2 = open(fastq2, "r")
            self.fastq2_size = os.path.getsize(fastq2)
        else:
            self.fastq2 = None
        self.nreads = nreads
        self.step = self.fastq1_size // nreads
        if self.step < 1:
            self.step = 1
        self.idx = iter(range(0, self.fastq1_size, self.step))
        self.n_sampled = 0
        self.read_ahead = 8  # read and increment 8 bytes at a time

    def __iter__(self):
        while self.n_sampled < self.nreads:
            i = next(self.idx)
            match = None
            while not match:
                self.fastq1.seek(i)
                if i + self.read_ahead > self.fastq1_size:
                    i = random.randrange(self.fastq1_size)
                match = re.search(self.pattern, self.fastq1.read(self.read_ahead))
                if match:
                    a, b = match.span()
                    self.read_ahead = (b - a) * 2
                    read1 = match.group(0)
                    if self.fastq2 is not None:
                        self.fastq2.seek(i + a)
                        read2 = self.fastq2.read(b - a)
                    else:
                        read2 = None
                    self.n_sampled += 1
                    yield (read1, read2)
                else:
                    self.read_ahead += self.read_ahead

    def __next__(self):
        return iter(self).next()

def run(args):
    sampler = FastqSampler(args.fastq1, args.fastq2, args.nreads, args.seed)
    for read1, read2 in sampler:
        args.out.write(read1)
        if read2 is not None:
            args.out2.write(read2)


def main():
    parser = argparse.ArgumentParser(prog='strandex', description="sample uniformly without reading an entire fastq file")
    parser.add_argument('fastq1', type=str, help="input fastq file")
    parser.add_argument('out', type=argparse.FileType('w'), help="output fastq file")
    parser.add_argument('-fq2', '--fastq2', type=str, help="input fastq file read pairs")
    parser.add_argument('-o2', '--out2', type=argparse.FileType('w'), help="output fastq file read pairs")
    parser.add_argument('-n', '--nreads', type=int, default=1, help='number of reads to sample from input (default: %(default)s)')
    parser.add_argument('-s', '--seed', type=float, default=random.random(), help='seed for random number generator (default: random)')
    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    main()
