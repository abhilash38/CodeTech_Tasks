import hashlib
import json
import os
import time

def calculate_file_hash(file_path, algorithm="sha256"):
    """Compute the hash of a file using the specified algorithm."""
    hasher = hashlib.new(algorithm)
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        print("File not found!")
        return None

def store_hash(file_path, hash_value):
    """Store the file's hash in a JSON file."""
    hash_data = {"file": file_path, "hash": hash_value}
    hash_file_path = f"{file_path}.hash.json"
    with open(hash_file_path, "w") as f:
        json.dump(hash_data, f, indent=4)
    print(f"Hash stored in {hash_file_path}")

def validate_file_integrity(file_path, new_hash):
    """Validate if the current hash matches the stored hash."""
    hash_file_path = f"{file_path}.hash.json"
    if os.path.exists(hash_file_path):
        with open(hash_file_path, "r") as f:
            stored_data = json.load(f)
            stored_hash = stored_data.get("hash")
            if stored_hash == new_hash:
                print("File integrity verified.")
            else:
                print("WARNING: File integrity compromised!")
    else:
        print("No stored hash found for comparison.")

def watch_file(file_path, interval=5, duration=30):
    """Monitor a file for any changes within a given duration."""
    print(f"Monitoring {file_path} for changes...")
    last_hash = calculate_file_hash(file_path)
    start_time = time.time()
    
    while time.time() - start_time < duration:
        time.sleep(interval)
        new_hash = calculate_file_hash(file_path)
        if new_hash and new_hash != last_hash:
            print(f"Change detected in {file_path}!")
            print(f"New hash: {new_hash}")
            last_hash = new_hash
        
    print("Monitoring completed.")

def main():
    file_path = input("Enter the file path to monitor: ")
    if not os.path.isfile(file_path):
        print("Invalid file path. Please try again.")
        return
    
    file_hash = calculate_file_hash(file_path)
    if file_hash:
        print(f"SHA-256 Hash: {file_hash}")
        store_hash(file_path, file_hash)
        validate_file_integrity(file_path, file_hash)
        watch_file(file_path, interval=5, duration=30)

if __name__ == "__main__":
    main()