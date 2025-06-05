# Mini-Projects

## 1) DNA Skew Diagram and Motif Finding Mini-Project

This mini-project implements algorithms for DNA sequence analysis to find the location of the chromosomal origin of replication (oriC) for *Salmonella enterica*.
Skew diagrams are used to identify regions of nucleotide bias that often mark the origin of replication, while pattern matching detects conserved dnaA box motifs near these regions. 

- **Skew diagrams** plot the cumulative difference between the occurrences of guanine (G) and cytosine (C) along the genome; since DNA replication tends to favor G on the leading strand and C on the lagging strand, the minimum point of the skew curve often corresponds to the origin of replication.

- **dnaA boxes** dnaA boxes are short, conserved DNA sequences typically 9 base pairs long that serve as binding sites for the DnaA protein, which initiates DNA replication at the origin by unwinding the DNA helix.


It primarily focuses on

---

### Features

- **SkewDiagram**: Computes cumulative G-C skew and finds minimal skew indices.
- **Approximate matching**: Locates pattern occurrences allowing mismatches.
- **Neighbor generation**: Enumerates all k-mers within d mismatches.
- **Frequent k-mer detection** with mismatches and reverse complements.
- **Clump finding** to detect overrepresented k-mers in genomic windows.
- Reading genome sequences from FASTA files.

---

### Results

Using the *Salmonella enterica* genome data, the following key results were obtained:

- **Minimal skew positions** (potential origins of replication) were identified at indices:  
  `[458745, 458746, 458747]`  
  These correspond to genomic regions with maximum G-C skew bias.

- **Frequent 9-mers with up to 1 mismatch** found in sliding windows (length 250 bp) that appear at least 5 times include:  
 `['TTATCCACA', 'TCATCCACA', 'TTATTCACA', 'TTATCCACC']`
These k-mers are consistent with known dnaA box motifs (Skovgaard O. and Hansen F.G., 1987), indicating likely replication initiation sites.

- The combined analysis of skew diagrams and clump-finding supports the prediction of functional replication origins in the genome.

---

## 2) PNG Decoder

A lightweight Python class for reading and processing raw `.png` image files that follow strict constraints:

- Bit depth: 8 bits per channel  
- Color type: 2 (Truecolor RGB)  
- Compression method: 0  
- Filter method: 0  
- Interlace method: 0 (no interlace)

## Features

- Validates PNG file format using the PNG signature  
- Extracts metadata: width, height, bit depth, color type, etc.  
- Reads and identifies PNG chunks (IHDR, IDAT, etc.)  
- Decompresses and reconstructs RGB pixel data  
- Enables saving of each of the Red, Green, or Blue channels into a separate file


## References

Skovgaard, O. and Hansen, F.G., 1987. Comparison of dnaA nucleotide sequences of Escherichia coli, Salmonella typhimurium, and Serratia marcescens. Journal of bacteriology, 169(9), pp.3976-3981.
