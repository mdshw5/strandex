# strandex
**strand**-anchored reg**ex** for uniform sampling from FASTQ files (think **spandex**)

[![Build Status](https://travis-ci.org/mdshw5/strandex.svg?branch=master)](https://travis-ci.org/mdshw5/strandex)
[![PyPI](https://img.shields.io/pypi/v/strandex.svg?branch=master)](https://pypi.python.org/pypi/strandex)
[![Landscape](https://landscape.io/github/mdshw5/strandex/master/landscape.svg)](https://landscape.io/github/mdshw5/strandex/master)
[![codecov](https://codecov.io/gh/mdshw5/strandex/branch/master/graph/badge.svg)](https://codecov.io/gh/mdshw5/strandex)


##Why use this?
- You want only a few reads from a large FASTQ file (**downsampling**)
- You are constrained by I/O so that reading through the entire file is very slow
- You want to avoid sampling only the beginning or end of the file
- You want to expand a small FASTQ file to a specific number of reads (**upsampling**)

# Install

`pip install strandex`

# Examples

```
from strandex import FastqSampler

sampler = FastqSampler('read1.fastq', fastq2='read2.fastq', nreads=100000, seed=42)
for read1, read2 in sampler:
  # read1 and read2 are 4-line strings sampled from paired input

sampler = FastqSampler('read1.fastq', nreads=100000, seed=42)
  for read1, read2 in sampler:
    # read1 is a 4-line string sampled from input
    # read2 is NoneType
```
Note that you may sample more reads *than are available in your input file*. In
the event that you want to sample more reads than your input file contains, strandex
will sample the file with replacement, meaning you will get some duplicate reads.

# CLI script

```
usage: strandex [-h] [-fq2 FASTQ2] [-o2 OUT2] [-n NREADS] [-s SEED] fastq1 out

sample uniformly without reading an entire fastq file

positional arguments:
  fastq1                input fastq file
  out                   output fastq file

optional arguments:
  -h, --help            show this help message and exit
  -fq2 FASTQ2, --fastq2 FASTQ2
                        input fastq file read pairs
  -o2 OUT2, --out2 OUT2
                        output fastq file read pairs
  -n NREADS, --nreads NREADS
                        number of reads to sample from input (default: 1)
  -s SEED, --seed SEED  seed for random number generator (default: None)
```
