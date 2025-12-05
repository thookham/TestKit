import json
import sqlite3
import os
from typing import List, Dict, Any

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'db', 'laptops.json')
DB_PATH = os.path.join(BASE_DIR, 'db', 'hardware.db')

def migrate() -> None:
    print(f"Migrating {JSON_PATH} to {DB_PATH}...")
    
    if not os.path.exists(JSON_PATH):
        print(f"Error: {JSON_PATH} not found.")
        return

    # Load JSON data
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        laptops = json.load(f)

    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS laptops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            year INTEGER,
            form_factor TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS supported_os (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            laptop_id INTEGER,
            os_name TEXT,
            FOREIGN KEY(laptop_id) REFERENCES laptops(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cpu_options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            laptop_id INTEGER,
            name TEXT,
            cores INTEGER,
            FOREIGN KEY(laptop_id) REFERENCES laptops(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ram_options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            laptop_id INTEGER,
            size_mb INTEGER,
            FOREIGN KEY(laptop_id) REFERENCES laptops(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS storage_options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            laptop_id INTEGER,
            size_gb INTEGER,
            FOREIGN KEY(laptop_id) REFERENCES laptops(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gpu_options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            laptop_id INTEGER,
            name TEXT,
            vram_mb INTEGER,
            FOREIGN KEY(laptop_id) REFERENCES laptops(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resolution_options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            laptop_id INTEGER,
            resolution TEXT,
            FOREIGN KEY(laptop_id) REFERENCES laptops(id)
        )
    ''')

    # Insert data
    for laptop in laptops:
        cursor.execute('''
            INSERT INTO laptops (make, model, year, form_factor)
            VALUES (?, ?, ?, ?)
        ''', (laptop.get('make'), laptop.get('model'), laptop.get('year'), laptop.get('form_factor')))
        
        laptop_id = cursor.lastrowid

        # Supported OS
        for os_name in laptop.get('supported_os', []):
            cursor.execute('INSERT INTO supported_os (laptop_id, os_name) VALUES (?, ?)', (laptop_id, os_name))

        # CPU Options
        for cpu in laptop.get('cpu_options', []):
            cursor.execute('INSERT INTO cpu_options (laptop_id, name, cores) VALUES (?, ?, ?)', (laptop_id, cpu.get('name'), cpu.get('cores')))

        # RAM Options
        for ram in laptop.get('ram_options', []):
            cursor.execute('INSERT INTO ram_options (laptop_id, size_mb) VALUES (?, ?)', (laptop_id, ram))

        # Storage Options
        for storage in laptop.get('storage_options', []):
            cursor.execute('INSERT INTO storage_options (laptop_id, size_gb) VALUES (?, ?)', (laptop_id, storage))

        # GPU Options
        for gpu in laptop.get('gpu_options', []):
            cursor.execute('INSERT INTO gpu_options (laptop_id, name, vram_mb) VALUES (?, ?, ?)', (laptop_id, gpu.get('name'), gpu.get('vram')))

        # Resolution Options
        for res in laptop.get('resolution_options', []):
            cursor.execute('INSERT INTO resolution_options (laptop_id, resolution) VALUES (?, ?)', (laptop_id, res))

    conn.commit()
    conn.close()
    print(f"Successfully migrated {len(laptops)} laptops to {DB_PATH}")

if __name__ == '__main__':
    migrate()
