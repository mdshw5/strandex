import os.path
import re
import sys
import argparse
import random
from six.moves import range

pattern = re.compile(r'(@.+)[\n\r]+.+[\n\r]+\+.*?[\n\r].+[\n\r]')

def run(args):

    file_size = os.path.getsize(args.fastq.name)
    random.seed(args.seed)
    n = 0
    ahead = 4096
    step = file_size // args.nreads
    if step < 1:
        step = 1
    idx = iter(range(0, file_size, step))
    while n < args.nreads:
        i = next(idx)
        match = None
        while not match:
            args.fastq.seek(i)
            if i + ahead > file_size:
                i = random.randrange(file_size)
            else:
                chunk = args.fastq.read(ahead)
            match = re.search(pattern, chunk)
            if match:
                a, b = match.span()
                ahead = int((ahead + (b - a) * 4) / 2)
                sys.stdout.write(match.group(0))
                n += 1
            else:
                ahead += ahead
    args.fastq.close()


def main():
    parser = argparse.ArgumentParser(prog='strandex', description="sample uniformly without reading an entire fastq file")
    parser.add_argument('fastq', type=argparse.FileType('r'), help="input fastq file")
    parser.add_argument('-n', '--nreads', type=int, default=1, help='number of reads to sample from input (default: %(default)s)')
    parser.add_argument('-s', '--seed', type=float, default=random.random(), help='seed for random number generator (default: None)')
    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    main()
