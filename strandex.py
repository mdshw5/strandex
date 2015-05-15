import os.path
from six.moves import range
import re
import sys
import argparse

pattern = re.compile(r'@.+[\n\r]+.+[\n\r]+\+.+[\n\r].+[\n\r]')

def run(args):
    file_size = os.path.getsize(args.fastq.name)
    step = file_size // args.nreads
    assert step > 0
    last_record = ''
    for i in range(0, file_size, step):
        match = None
        ahead = 4000
        while not match:
            args.fastq.seek(i)
            if i + ahead > file_size:
                break
            else:
                chunk = args.fastq.read(ahead)
            match = re.search(pattern, chunk)
            if match:
                start, end = match.span()
                record = chunk[start:end]
                if record != last_record:
                    sys.stdout.write(record)
                last_record = record
            else:
                ahead += ahead
    args.fastq.close()


def main():
    parser = argparse.ArgumentParser(prog='strandex', description="sample an approximate number of reads from a fastq file without reading the entire file")
    parser.add_argument('fastq', type=argparse.FileType('r'), help="input fastq file")
    parser.add_argument('-n', '--nreads', type=int, default=2000000, help='approximate number of reads to sample from input (default: %(default)s)')
    args = parser.parse_args()
    run(args)

if __name__ == "__main__":
    main()
