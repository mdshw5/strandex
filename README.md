# strandex
**strand**-anchored reg**ex** for **ex**pansion or contraction of FASTQ files (think **spandex**)

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

##Why use this?
- You want only a few reads from a large FASTQ file (**downsampling**)
- You are constrained by I/O so that reading through the entire file is very slow
- You want to avoid sampling only the beginning or end of the file
- You want to expand a small FASTQ file to a specific number of reads (**upsampling**)
