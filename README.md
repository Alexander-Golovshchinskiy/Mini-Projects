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


