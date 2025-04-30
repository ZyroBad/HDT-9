
# David Sebastian Lemus Nitsch (241155)
# Luis Alejandro Hernández Márquez (241424)
# Sección: 20

import heapq
import os
import pickle
from collections import defaultdict, Counter

class HuffmanNode:
    def _init_(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def _lt_(self, other):
        return self.freq < other.freq

def build_frequency_table(text):
    return Counter(text)

def build_huffman_tree(freq_table):
    priority_queue = [HuffmanNode(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0] if priority_queue else None

def build_codes(root):
    codes = {}

    def traverse(node, path):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = path
        traverse(node.left, path + "0")
        traverse(node.right, path + "1")

    traverse(root, "")
    return codes

def encode_text(text, codes):
    return ''.join(codes[char] for char in text)

def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    encoded_text += "0" * extra_padding
    padded_info = f"{extra_padding:08b}"
    return padded_info + encoded_text

def get_byte_array(padded_encoded_text):
    return bytearray(int(padded_encoded_text[i:i+8], 2) for i in range(0, len(padded_encoded_text), 8))

def compress(input_path):
    if not os.path.exists(input_path):
        print(f"Error: El archivo '{input_path}' no fue encontrado.")
        return

    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()

    freq_table = build_frequency_table(text)
    root = build_huffman_tree(freq_table)
    codes = build_codes(root)
    encoded_text = encode_text(text, codes)
    padded_textl = pad_encoded_text(encoded_text)
    byte_array = get_byte_array(padded_textl)

    with open(input_path + '.huff', 'wb') as output:
        output.write(byte_array)

    with open(input_path + '.hufftree', 'wb') as tree_file:
        pickle.dump(root, tree_file)
        
def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)
    return padded_encoded_text[8:-extra_padding]

def decode_text(encoded_text, root):
    decoded_text = []
    current = root
    for bit in encoded_text:
        current = current.left if bit == "0" else current.right
        if current.char is not None:
            decoded_text.append(current.char)
            current = root
    return ''.join(decoded_text)

def decompress(huff_path, tree_path):
    if not os.path.exists(huff_path):
        print(f"Error: El archivo '{huff_path}' no fue encontrado.")
        return
    if not os.path.exists(tree_path):
        print(f"Error: El archivo '{tree_path}' no fue encontrado.")
        return

    with open(huff_path, 'rb') as file:
        bit_string = "".join(f"{byte:08b}" for byte in file.read())

    with open(tree_path, 'rb') as tree_file:
        root = pickle.load(tree_file)

    encoded_text = remove_padding(bit_string)
    decompressed_text = decode_text(encoded_text, root)

    output_path = huff_path.replace('.huff', '.decoded.txt')
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(decompressed_text)

    return output_path


archivo = "ejemplo.txt"

compress(archivo)

if os.path.exists(archivo + ".huff") and os.path.exists(archivo + ".hufftree"):
    salida = decompress(archivo + ".huff", archivo + ".hufftree")
    if salida:
        print(f"Archivo descomprimido: {salida}")