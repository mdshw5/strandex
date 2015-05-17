# strandex
**strand**-anchored reg**ex** for **ex**pansion or contraction of FASTQ files (think **spandex**)

```
usage: strandex [-h] [-n NREADS] [-s SEED] fastq

sample uniformly without reading an entire fastq file

positional arguments:
  fastq                 input fastq file

optional arguments:
  -h, --help            show this help message and exit
  -n NREADS, --nreads NREADS
                        number of reads to sample from input (default: 1)
  -s SEED, --seed SEED  seed for random number generator (default: None)
```

##Why use this?
- You want only a few reads from a large FASTQ file (**downsampling**)
- You are constrained by I/O so that reading through the entire file is very slow
- You want to avoid sampling only the beginning or end of the file
- You want to expand a small FASTQ file to a specific number of reads (**upsampling**)
