import os.path
import re
import sys
import argparse
import random
import fastq
from six.moves import range

pattern = re.compile(r'@.+[\n\r]+.+[\n\r]+\+.*?[\n\r].+[\n\r]')
__version__ = "0.1"

def run(args):
    # Determine read size in bytes
    with fastq.Reader(args.fastq1.name) as fq1:
        read_size = len(str(next(fq1)))
    # Determine file size in bytes
    file_size = os.path.getsize(args.fastq1.name)
    random.seed(args.seed)
    n = 0
    slop = 0
    ahead = read_size * 2
    step = file_size // args.nreads
    if step < 1:
        step = 1
    idx = iter(range(0, file_size, step))
    while n < args.nreads:
        i = next(idx)
        match = None
        while not match:
            args.fastq1.seek(i)
            if i + ahead > file_size:
                i = random.randrange(file_size)
            else:
                chunk = args.fastq1.read(ahead)
            match = re.search(pattern, chunk)
            if match:
                a, b = match.span()
                ahead = (b - a) * 2
                args.out.write(match.group(0))
                if args.fastq2:
                    args.fastq2.seek(i + a)
                    args.out2.write(args.fastq2.read(b-a))
                n += 1
            else:
                ahead += ahead



def main():
    parser = argparse.ArgumentParser(prog='strandex', description="sample uniformly without reading an entire fastq file")
    parser.add_argument('fastq1', type=argparse.FileType('r'), help="input fastq file")
    parser.add_argument('out', type=argparse.FileType('w'), help="output fastq file")
    parser.add_argument('-fq2', '--fastq2', type=argparse.FileType('r'), help="input fastq file read pairs")
    parser.add_argument('-o2', '--out2', type=argparse.FileType('w'), help="output fastq file read pairs")
    parser.add_argument('-n', '--nreads', type=int, default=1, help='number of reads to sample from input (default: %(default)s)')
    parser.add_argument('-s', '--seed', type=float, default=random.random(), help='seed for random number generator (default: None)')
    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    main()
