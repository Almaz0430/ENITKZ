#!/usr/bin/env python
import base64
import hashlib
import os
import sys

def generate_sri_hash(file_path):
    """Генерирует SRI-хеш для файла."""
    with open(file_path, 'rb') as file:
        content = file.read()
        hash_obj = hashlib.sha384(content)
        hash_base64 = base64.b64encode(hash_obj.digest()).decode('utf-8')
        return f"sha384-{hash_base64}"

def main():
    """Основная функция для генерации SRI-хешей для файлов."""
    if len(sys.argv) < 2:
        print("Использование: python generate_sri_hashes.py <путь_к_файлу>")
        return
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return
    
    sri_hash = generate_sri_hash(file_path)
    print(f"SRI-хеш для {os.path.basename(file_path)}: {sri_hash}")

if __name__ == "__main__":
    main() 