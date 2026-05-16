class CompressionError(Exception):
    """General compression error."""
    pass

class DecompressionError(Exception):
    """General decompression error."""
    pass

class InvalidFileFormatError(Exception):
    """Raised when an unsupported or malformed file is encountered."""
    pass

class MetadataMismatchError(Exception):
    """Raised when metadata doesn't match binary archive."""
    pass
