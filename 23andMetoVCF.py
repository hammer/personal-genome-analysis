from Bio import SeqIO

# Read a 23andMe file
infile = open("genome_Jeff_Hammerbacher_Full_20130125202523.txt", "r")

# Skip comments
line = infile.readline()  
while (line.startswith('#')):
  line = infile.readline()

# Write a VCF file
outfile = open("my_genome.vcf", "w")
outfile.write("""\
##fileformat=VCFv4.1
##fileDate=20130131
##source=23andMetoVCF.py
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	GENOTYPE
""")

current_chromosome = ''
while line:
  rsid, chromosome, position, genotype = line.split()

  if (chromosome != current_chromosome):
    # 23andMe and UCSC naming convention diverges for mitochondrial DNA
    chromosome_file_suffix = chromosome
    if (chromosome == 'MT'):
      chromosome_file_suffix = 'M'
    # Load up the new chromosome
    current_chromosome_sequence = SeqIO.read(open("GRCh37/chr%s.fa" % chromosome_file_suffix, "rU"), "fasta")
    current_chromosome = chromosome

  # because python arrays are 0-indexed
  reference_genotype = current_chromosome_sequence[int(position) - 1].upper() 

  # GT coding
  # TODO(hammer): handle the X chromosome genotypes where I have a single base
  # TODO(hammer): handle the case where I'm heterozygous with two bases different from the reference (comma-separated in ALT, higher numbers in GENOTYPE)
  # TODO(hammer): handle "--" genotype call from 23andMe (use "./." in GENOTYPE)
  allele1 = genotype[0].upper()
  allele2 = genotype[1].upper()

  GT1 = 0
  GT2 = 0

  alt = "."
  if (reference_genotype != allele1):
    alt = allele1
    GT1 = 1
  if (reference_genotype != allele2):
    alt = allele2
    GT2 = 1

  vcf_data = ["chr" + chromosome_file_suffix,
              position,
              rsid,
              reference_genotype,
              alt,
              ".",
              ".",
              ".",
              "GT",
              "%d/%d" % (GT1, GT2),
              ]
  outfile.write("\t".join(vcf_data) + "\n")

  line = infile.readline()

outfile.close()
