import chardet
from unidecode import unidecode

def decode_file(file_bytes: bytes) -> str:
    "Detect the encoding of a byte stream and convert it to a UTF-8 string"
    encoding = chardet.detect(file_bytes)
    print("Detected encoding: {}".format(encoding))
    utf8str = file_bytes.decode(encoding["encoding"])
    return unidecode(utf8str)
