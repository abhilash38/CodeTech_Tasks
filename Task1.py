import hashlib
import json
import os
import time

def calculate_file_hash(file_path, algorithm="sha256"):
    """Compute the hash of a file using the specified algorithm."""
    try:
        hasher = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        print("Error: File not found!")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def store_hash(file_path, hash_value):
    """Store the file's hash in a JSON file."""
    hash_data = {"file": file_path, "hash": hash_value}
    hash_file_path = f"{file_path}.hash.json"
    try:
        with open(hash_file_path, "w") as f:
            json.dump(hash_data, f, indent=4)
        print(f"Hash stored in {hash_file_path}")
    except Exception as e:
        print(f"Failed to store hash: {e}")

def validate_file_integrity(file_path, current_hash):
    """Validate if the current hash matches the stored hash."""
    hash_file_path = f"{file_path}.hash.json"
    if not os.path.exists(hash_file_path):
        print("No stored hash found for comparison.")
        return False

    try:
        with open(hash_file_path, "r") as f:
            stored_data = json.load(f)
        stored_hash = stored_data.get("hash")
        if stored_hash == current_hash:
            print("File integrity verified.")
            return True
        else:
            print("WARNING: File integrity compromised!")
            return False
    except Exception as e:
        print(f"Error reading hash file: {e}")
        return False

def watch_file(file_path, interval=5, duration=30):
    """Monitor a file for any changes within a given duration."""
    print(f"Monitoring {file_path} for changes (every {interval}s for {duration}s)...")
    last_hash = calculate_file_hash(file_path)
    if last_hash is None:
        return

    start_time = time.time()

    try:
        while time.time() - start_time < duration:
            time.sleep(interval)
            new_hash = calculate_file_hash(file_path)
            if new_hash is None:
                print(f"File {file_path} is no longer accessible.")
                break

            if new_hash != last_hash:
                print(f"Change detected in {file_path}!")
                print(f"New hash: {new_hash}")
                last_hash = new_hash
        print("Monitoring completed.")
    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user.")

def main():
    file_path = input("Enter the file path to monitor: ").strip()
    file_path = os.path.abspath(file_path)

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
