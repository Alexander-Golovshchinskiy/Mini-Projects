# Mini-Projects
Code for mini-projects - both related or unrelated to biology.


## 1) PNG Decoder

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
- Enables saving of each of the R, G, B channels into a separate file


## DNA Skew Diagram and Motif Finding Mini-Project

This mini-project implements algorithms for DNA sequence analysis, focusing on:

- Calculating **skew diagrams** to find regions of nucleotide bias (G vs C) which can help locate origins of replication.
- Computing **Hamming distance** to allow approximate pattern matching.
- Finding **approximate matches** of DNA patterns with mismatches.
- Generating **neighbors** (all possible k-mers within a mismatch distance).
- Detecting **most frequent k-mers** with mismatches and reverse complements.
- Finding **(L, t, d)-clumps**: k-mers that appear frequently with mismatches in sliding windows.
- Combining skew and clump analysis to predict functional genomic regions such as DnaA boxes.

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
These k-mers are consistent with known DnaA box motifs, indicating likely replication initiation sites.

- The combined analysis of skew diagrams and clump-finding supports the prediction of functional replication origins in the genome.

---
