import os
import pytest
from HDT9 import compress, decompress

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def remove_files(*files):
    for f in files:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

def test_huffman_compression_long_text(tmp_path):
    test_text = (
        "Este es un texto de prueba para verificar si el algoritmo de compresi\u00f3n Huffman "
        "funciona correctamente y puede restaurar el contenido original sin p\u00e9rdida de datos."
    )
    input_file = tmp_path / "entrada.txt"
    write_file(input_file, test_text)

    compress(str(input_file))
    decompress(str(input_file) + ".huff", str(input_file) + ".hufftree")

    decoded_file = input_file.with_name("entrada.txt.decoded.txt")
    assert read_file(decoded_file) == test_text

def test_huffman_compression_short_text(tmp_path):
    test_text = "aaaaabbbbcc"
    input_file = tmp_path / "simple.txt"
    write_file(input_file, test_text)

    compress(str(input_file))
    decompress(str(input_file) + ".huff", str(input_file) + ".hufftree")

    decoded_file = input_file.with_name("simple.txt.decoded.txt")
    assert read_file(decoded_file) == test_text

def test_huffman_compression_empty_file(tmp_path):
    input_file = tmp_path / "vacio.txt"
    write_file(input_file, "")

    compress(str(input_file))
    decompress(str(input_file) + ".huff", str(input_file) + ".hufftree")

    decoded_file = input_file.with_name("vacio.txt.decoded.txt")
    assert read_file(decoded_file) == ""

    # Limpieza (opcional)
    remove_files(input_file, str(input_file) + ".huff", str(input_file) + ".hufftree", decoded_file)
