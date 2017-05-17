import os.path
import re
import sys
import argparse
import random
from six.moves import range
from six import string_types

__version__ = "0.4.1"

class Fastq(object):
    """
    A class to hold features from fastq reads.
    """
    def __init__(self, name='', seq='', strand='+', qual=''):
        self.name = name
        self.seq = seq
        self.strand = strand
        self.qual = qual
        self.i = int()
        assert isinstance(name, string_types)
        assert isinstance(seq, string_types)
        assert isinstance(qual, string_types)

    def __iter__(self):
        return self

    def next(self):
        if self.i < len(self):
            value, self.i = self[self.i], self.i + 1
            return value
        else:
            raise StopIteration()

    def __getitem__(self, key):
        return self.__class__(self.name, self.seq[key], self.strand, self.qual[key])

    def __next__(self):
        return self.next()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n'.join([self.name, self.seq, self.strand, self.qual]) + '\n'

    def __len__(self):
        return len(self.seq)

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

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.fastq1.close()
        if self.fastq2 is not None:
            self.fastq2.close()

def run(args):
    sampler = FastqSampler(args.fastq1, args.fastq2, args.nreads, args.seed)
    for read1, read2 in sampler:
        read1 = Fastq(*read1.rstrip().split('\n'))
        if read2:
            read2 = Fastq(*read2.rstrip().split('\n'))
        if args.trim:
            assert len(read1) >= args.trim
        args.out.write(str(read1[:args.trim]))
        if read2 is not None:
            args.out2.write(str(read2[:args.trim]))


def main():
    parser = argparse.ArgumentParser(prog='strandex', description="sample uniformly without reading an entire fastq file")
    parser.add_argument('fastq1', type=str, help="input fastq file")
    parser.add_argument('out', type=argparse.FileType('w'), help="output fastq file")
    parser.add_argument('-fq2', '--fastq2', type=str, help="input fastq file read pairs")
    parser.add_argument('-o2', '--out2', type=argparse.FileType('w'), help="output fastq file read pairs")
    parser.add_argument('-n', '--nreads', type=int, default=1, help='sample -n reads from input files (default: %(default)s)')
    parser.add_argument('-s', '--seed', type=float, default=random.random(), help='seed for random number generator (default: random)')
    parser.add_argument('-t', '--trim', type=int, default=None, help='trim reads to length -t (default: %(default)s)')
    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    main()
