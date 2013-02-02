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
outfile.close()

current_chromosome = ""
while line:
  rsid, chromosome, position, genotype = line.split()

  if (chromosome != current_chromosome):
    # 23andMe and UCSC naming convention diverges for mitochondrial DNA
    chromosome_file_suffix = chromosome
    if (chromosome == "MT"):
      chromosome_file_suffix = "M"
    # Load up the new chromosome
    current_chromosome_sequence = SeqIO.read(open("GRCh37/chr%s.fa" % chromosome_file_suffix, "rU"), "fasta")
    current_chromosome = chromosome

  # because python arrays are 0-indexed
  reference_genotype = current_chromosome_sequence[int(position) - 1].upper() 

  # GT coding
  # TODO(hammer): distinguish between X chromosome loci where there are two bases rather than a single base
  alt = []
  vcf_genotype = []

  if (chromosome == "X"):
    # Not sure how to handle yet; see http://www.biostars.org/p/62635/
    line = infile.readline()
    continue
  elif (chromosome in ["Y", "MT"]):
    if (genotype == "--"):
      alt.append(".")
      vcf_genotype.append(".")
    else:
      allele = genotype.upper()
      if (reference_genotype != allele):
        alt.append(allele)
        vcf_genotype.append("1")
      else:
        alt.append(".")
        vcf_genotype.append("0")
  else:
    if (genotype == "--"):
      alt.append(".")
      vcf_genotype.extend([".", "."])
    else:
      alleles = [genotype[0].upper(), genotype[1].upper()]
      if (reference_genotype != alleles[0] and reference_genotype != alleles[1]):
        if (alleles[0] == alleles[1]):
          alt.append(alleles[0])
          vcf_genotype.extend(["1", "1"])
        else:
          alt.extend(alleles)
          vcf_genotype.extend(["1", "2"])
      elif (reference_genotype == alleles[0] and reference_genotype == alleles[1]):
        alt.append(".")
        vcf_genotype.extend(["0", "0"])
      elif (reference_genotype != alleles[0]):
        alt.append(alleles[0])
        vcf_genotype.extend(["1", "0"])
      else:
        alt.append(alleles[1])
        vcf_genotype.extend(["0", "1"])

  # Serialize new row in VCF file
  vcf_data = ["chr" + chromosome_file_suffix,
              position,

              rsid,
              reference_genotype,
              ",".join(alt),
              ".",
              ".",
              ".",
              "GT",
              "/".join(vcf_genotype),
              ]
  # open and close file because things seem to be messed up if it's open too long
  outfile = open("my_genome.vcf", "a")
  outfile.write("\t".join(vcf_data) + "\n")
  outfile.close()

  line = infile.readline()

outfile.close()
