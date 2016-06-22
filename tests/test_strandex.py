import os
from unittest import TestCase
from subprocess import check_call
from shlex import split
from nose.tools import nottest

class TestStrandex(TestCase):
    @classmethod
    def setUpClass(self):
        """ Downloading test data """
        check_call('curl -s http://ftp.sra.ebi.ac.uk/vol1/fastq/ERR239/ERR239653/ERR239653_1.fastq.gz | gzip -dcq | head -n 400000 > test1.fastq', shell=True)
        check_call('curl -s http://ftp.sra.ebi.ac.uk/vol1/fastq/ERR239/ERR239653/ERR239653_2.fastq.gz | gzip -dcq | head -n 400000 > test2.fastq', shell=True)
        self.fastq1 = 'test1.fastq'
        self.fastq2 = 'test2.fastq'

    @classmethod
    def tearDownClass(self):
        os.remove(self.fastq1)
        os.remove(self.fastq2)

    def test_sampler_fragment(self):
        from strandex import FastqSampler
        sampler = FastqSampler(self.fastq1)
        read1, read2 = next(iter(sampler))
        print(read1)
        print(read2)
        assert read1 == '@ERR239653.1 HS28_09354:1:1101:1150:32544#54/1\nTAGGCTGGTCTCCAATTCCTGAGCTCAAGCAATCCTCCTACCTCAGACTCCCAAAGTGCTGGGATTACGAGAGTAAGCCACTGTNCNNNGCCAAAACAAG\n+\n=DDEEFFEFGGCFAFEGDFFI@HAFDCEFF?FGEEHFHFGGIGGDEGBE.I=DIGHBH<EFBGCGEFHCGGEE9B-5EBDFDID!G!!!GCFEE9GGGH:\n'
        assert read2 == None

    def test_sampler_paired(self):
        from strandex import FastqSampler
        sampler = FastqSampler(self.fastq1, fastq2=self.fastq2)
        read1, read2 = next(iter(sampler))
        print(read1)
        print(read2)
        assert read1 == '@ERR239653.1 HS28_09354:1:1101:1150:32544#54/1\nTAGGCTGGTCTCCAATTCCTGAGCTCAAGCAATCCTCCTACCTCAGACTCCCAAAGTGCTGGGATTACGAGAGTAAGCCACTGTNCNNNGCCAAAACAAG\n+\n=DDEEFFEFGGCFAFEGDFFI@HAFDCEFF?FGEEHFHFGGIGGDEGBE.I=DIGHBH<EFBGCGEFHCGGEE9B-5EBDFDID!G!!!GCFEE9GGGH:\n'
        assert read2 == '@ERR239653.1 HS28_09354:1:1101:1150:32544#54/2\nGTCTCAANTNCCTGGCTTCAAATGATCCTCCTGTCTTGGCCTTCCAAAGTGCTTGGATTACAGGTGTAAGCCACCATGACTGGCCAGAAATTTCCACCTT\n+\n?DDDBED!=!=GFGFCGIDDEFGEFGCHHGCIFDGIG@GDGFGDG:@;DGGFGFFG?GHGDGGGCDIFFH8GHHEEHFFEEHHHF7FAI8,CEFFE8FHG\n'

    def test_sampler_consistency(self):
        from strandex import FastqSampler
        sampler = FastqSampler(self.fastq1, fastq2=self.fastq2, nreads=200, seed=42)
        for read1, read2 in sampler:
            assert read1.split('\n')[0].replace('/1', '') == read2.split('\n')[0].replace('/2', '')

    def test_sampler_consistency_oversample(self):
        from strandex import FastqSampler
        sampler = FastqSampler(self.fastq1, fastq2=self.fastq2, nreads=200000, seed=42)
        for read1, read2 in sampler:
            assert read1.split('\n')[0].replace('/1', '') == read2.split('\n')[0].replace('/2', '')

    @nottest
    def test_sampler_full_sample(self):
        from strandex import FastqSampler
        from strandex.fastq import Reader
        sampler = FastqSampler(self.fastq1, fastq2=self.fastq2, nreads=100000, seed=42)
        with Reader(self.fastq1) as fq1, Reader(self.fastq2) as fq2:
            for (sample1, sample2), read1, read2 in zip(sampler, fq1, fq2):
                print(sample1)
                print(read1)
                assert sample1 == str(read1)
                assert sample2 == str(read2)

    def test_sampler_no_oversample(self):
        from strandex import FastqSampler
        seen = []
        sampler = FastqSampler(self.fastq1, fastq2=self.fastq2, nreads=80000, seed=42)
        for read1, read2 in sampler:
            read_name = read1.split('\n')[0].replace('/1', '')
            assert read_name not in seen
            seen.append(read_name)
