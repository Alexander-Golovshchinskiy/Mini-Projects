import math 
import zlib

class PNG:
    """
    A class for processing PNG files with specific properties:
    - Bit depth: 8 bits per channel
    - Color type: 2 (Truecolor, RGB)
    - Compression method: 0
    - Filter method: 0
    - Interlace method: 0 (No interlace)

    This class supports:
    - Validating PNG files via their signature and structure.
    - Extracting metadata such as width, height, and color type.
    - Decompressing and reconstructing RGB image data.
    - Saving modified PNG images with specific RGB channels.

    Key Attributes:
    - REFERENCE_SEQUENCES: Predefined hex sequences for PNG structure (e.g., signature, chunks).
    - SIGN_START, SIGN_FIN: Byte indices for validating the PNG signature.
    - IHDR_START, IHDR_FIN: Byte indices for locating and processing the IHDR chunk.

    Key Constants:
    - SUB_FILTER, UP_FILTER, AVERAGE_FILTER, PAETH_FILTER: Filter method codes.

    References:
    - PNG (Portable Network Graphics) Specification: https://www.w3.org/TR/PNG/
    """

    REFERENCE_SEQUENCES = {
        'SIGNATURE': ['89', '50', '4E', '47', '0D', '0A', '1A', '0A'],
        'IHDR': ['49', '48', '44', '52'],
        'PLTE': ['50', '4C', '54', '45'],
        'IDAT': ['49', '44', '41', '54'],
        'IEND': ['49', '45', '4E', '44']
    }

    SIGN_START, SIGN_FIN = 0, 8
    IHDR_START, IHDR_FIN = 8, 12

    SUB_FILTER = 1
    UP_FILTER = 2
    AVERAGE_FILTER = 3
    PAETH_FILTER = 4

    def __init__(self):
        self.data = bytes()          # Raw PNG file data
        self.info = str()            # File information or error messages
        self.width = int()           # Image width
        self.height = int()          # Image height
        self.bit_depth = int()       # Bit depth per channel
        self.color_type = int()      # PNG color type (e.g., 2 for truecolor)
        self.compress = int()        # Compression method
        self.filter = int()          # Filter method
        self.interlace = int()       # Interlace method
        self.img = list()            # Reconstructed RGB image data
        self.window = [0, 0]         # Current byte range being processed
        self.signature = list()      # PNG signature for validation
        self.reconstructed = list()  # List for reconstruction step

    def bytes_to_hex(self, data, window):
        """Converts bytes in a given window to a list of hexadecimal strings."""
        return [f'{byte:02X}' for byte in data[window[0]:window[1]]]

    def update_window(self, offset):
        """Moves window further by the value equal to offset"""
        self.window[0] += offset
        self.window[1] += offset

    def bytes_to_int(self, data, window):
        """Converts bytes in a given window to an integer."""
        return int(''.join(self.bytes_to_hex(data, window)), 16)
    
    def type_to_bytes(self, chunk_type):
        '''Converts type from reference format to bytearray'''
        return bytearray(int(num, 16) for num in self.REFERENCE_SEQUENCES[chunk_type])

    def load_file(self, file_name):
        """Load a PNG file into the class instance."""
        try:
            with open(file_name, 'rb') as loaded_png:
                self.info = file_name
                self.data = loaded_png.read()
        except FileNotFoundError:
            self.info = 'file not found'
            self.data = b''

    def valid_png(self):
        """Check if the loaded file is a valid PNG based on its signature."""

        if not self.data:
            raise ValueError("File is missing or empty. Cannot validate PNG.")
        
        self.window[0], self.window[1] = self.SIGN_START, self.SIGN_FIN
        self.signature = self.bytes_to_hex(self.data, self.window)
        return self.signature == self.REFERENCE_SEQUENCES['SIGNATURE']

    def read_header(self):
        """Read the IHDR chunk (header) to extract image metadata."""

        if not self.valid_png():
            raise ValueError("Cannot read header: Invalid PNG file.")
        
        self.window[0], self.window[1] = self.IHDR_START, self.IHDR_FIN
        self.header_length = self.bytes_to_int(self.data, self.window)

        # Width
        self.window[0] = self.IHDR_START + 8
        self.window[1] = self.IHDR_FIN + 8
        self.width = self.bytes_to_int(self.data, self.window)

        # Height
        self.update_window(4)
        self.height = self.bytes_to_int(self.data, self.window)

        # Bit depth
        self.window[0] += 4
        self.window[1] += 1
        self.bit_depth = self.bytes_to_int(self.data, self.window)

        # Color type
        self.update_window(1)
        self.color_type = self.bytes_to_int(self.data, self.window)

        # Compression, filter, and interlace methods
        self.update_window(1)
        self.compression = self.bytes_to_int(self.data, self.window)
        self.update_window(1)
        self.filter = self.bytes_to_int(self.data, self.window)
        self.update_window(1)
        self.interlace = self.bytes_to_int(self.data, self.window)

    def read_chunks(self):
        """
        Process chunks to extract image data from IDAT chunks, 
        decompress it, and reconstruct RGB pixel values.
        """

        if not self.valid_png():
            raise ValueError("Cannot read chunks: Invalid PNG file.")

        self.compressed_data = b''
        self.decompressed_data = b''

        #move window to the start of the chunk following the IHDR
        self.window[0] = self.IHDR_START + self.header_length + 12
        self.window[1] = self.IHDR_FIN + self.header_length + 12

        while True:
            #read length
            self.chunk_length = self.bytes_to_int(self.data, self.window)

            #move to type
            self.update_window(4)

            #IEND found
            if self.bytes_to_hex(self.data, self.window) == self.REFERENCE_SEQUENCES['IEND']:
                self.compressed_data = self.compressed_data.rstrip(b'\x00') #strip trailing zeroes from data
                break 

            #Ancillary chunk found
            if self.bytes_to_hex(self.data, self.window) != self.REFERENCE_SEQUENCES['IDAT']:
                self.update_window(self.chunk_length + 8)  # Skip non-IDAT chunks
                continue
            
            #move to data
            self.window[0] += 4
            self.window[1] = self.window[0] + self.chunk_length

            #add if data is not empty
            if self.window[0] != self.window[1]:
                self.compressed_data += self.data[self.window[0]:self.window[1]]

            #move to start of the next chunk
            self.window[0] += self.chunk_length + 4
            self.window[1] += 8

        try:
            self.decompressed_data = zlib.decompress(self.compressed_data)
        except zlib.error as e:
            print(f'Decompression error: {e}')

        def apply_filter(filter_type, scanline):

            def paeth_predictor(a, b, c):
                p = a + b - c
                pa = abs(p - a)
                pb = abs(p - b)
                pc = abs(p - c)
                if pa <= pb and pa <= pc:
                    return a
                elif pb <= pc:
                    return b
                return c
            
            if filter_type == self.SUB_FILTER:  
                for i in range(len(scanline)):
                    left = scanline[i - 3] if i >= 3 else 0
                    scanline[i] = (scanline[i] + left) % 256

            elif filter_type == self.UP_FILTER:  
                if len(self.reconstructed) > 0: #not first row
                    above_row = self.reconstructed[-1]
                    for i in range(len(scanline)):
                        above = above_row[i]
                        scanline[i] = (scanline[i] + above) % 256

            elif filter_type == self.AVERAGE_FILTER:  
                if len(self.reconstructed) > 0: #not first row
                    above_row = self.reconstructed[-1]
                    for i in range(len(scanline)):
                        left = scanline[i - 3] if i >= 3 else 0
                        above = above_row[i]
                        scanline[i] = (scanline[i] + ((left + above) // 2)) % 256
                else: #first row
                    for i in range(len(scanline)):
                        left = scanline[i - 3] if i >= 3 else 0
                        scanline[i] = (scanline[i] + (left // 2)) % 256

            elif filter_type == self.PAETH_FILTER:  
                if len(self.reconstructed) > 0: #not first row 
                    above_row = self.reconstructed[-1]
                    for i in range(len(scanline)):
                        left = scanline[i - 3] if i >= 3 else 0
                        above = above_row[i]
                        top_left = above_row[i - 3] if i >= 3 else 0
                        predictor = paeth_predictor(left, above, top_left)
                        scanline[i] = (scanline[i] + predictor) % 256
                else: #first row
                    for i in range(len(scanline)):
                        left = scanline[i - 3] if i >= 3 else 0
                        predictor = paeth_predictor(left, 0, 0)
                        scanline[i] = (scanline[i] + predictor) % 256

            return scanline

        bytes_per_pixel = 3
        scanline_len = self.width * bytes_per_pixel

        #reconstruction
        for row_start in range(0, len(self.decompressed_data), scanline_len + 1):
            filter_type = self.decompressed_data[row_start]
            scanline = bytearray(self.decompressed_data[row_start + 1 : row_start + scanline_len + 1])
            reconstructed_scanline = apply_filter(filter_type, scanline)
            self.reconstructed.append(reconstructed_scanline)

        #3-d array to store RGB values
        for row in self.reconstructed:
            rgb_row = []
            for i in range(0, len(row), 3):
                rgb_row.append([row[i], row[i + 1], row[i + 2]])
            self.img.append(rgb_row)

    def save_rgb(self, file_name, rgb_option):
        """Save a modified PNG file with a single RGB channel based on the given option."""

        if rgb_option not in [1, 2, 3]:
            raise ValueError(f"Invalid RGB option {rgb_option}. Must be 1 (Red), 2 (Green), or 3 (Blue).")
        
        channel = rgb_option - 1
        width = len(self.img[0])
        height = len(self.img)
        raw_data = bytearray()

        for row in self.img:
            raw_data.append(0)  # Filter type 0
            for pixel in row:
                for i, value in enumerate(pixel):
                    value_to_append = value if i == channel else 0
                    raw_data.append(value_to_append)

        compressed = zlib.compress(raw_data)

        #add any chunk to a file
        def write_chunk(file, chunk_type, chunk_data):
            chunk_length = len(chunk_data)
            chunk_type_bytes = self.type_to_bytes(chunk_type)
            crc = zlib.crc32(chunk_type_bytes + chunk_data)

            file.write(chunk_length.to_bytes(4, 'big'))
            file.write(chunk_type_bytes)
            file.write(chunk_data)
            file.write(crc.to_bytes(4, 'big'))

        with open(file_name, 'wb') as f:
            f.write(self.type_to_bytes('SIGNATURE'))

            ihdr_data = (
                width.to_bytes(4, byteorder='big') +  # Width (4 bytes)
                height.to_bytes(4, byteorder='big') +  # Height (4 bytes)
                b'\x08' +  # Bit depth (1 byte, 8 bits per channel)
                b'\x02' +  # Color type (1 byte, truecolour)
                b'\x00' +  # Compression method (1 byte)
                b'\x00' +  # Filter method (1 byte)
                b'\x00'  # Interlace method (1 byte)
            )

            idat_data = compressed 
            iend_data = b'' 
            write_chunk(f, 'IHDR', ihdr_data)
            write_chunk(f, 'IDAT', idat_data)
            write_chunk(f, 'IEND', iend_data)