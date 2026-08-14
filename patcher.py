import os

def run_hex_patcher():
    metadata_path = os.path.join("RecRoom_Data", "Managed", "Metadata", "global-metadata.dat")
    assembly_path = "GameAssembly.dll"
    
    targets = [metadata_path, assembly_path]
    replacements = {
        b"https://rec.net": b"http://127.0.0.1:8080",
        b"https://rec.net": b"http://127.0.0.1:8080"
    }
    
    for path in targets:
        if not os.path.exists(path):
            continue
            
        print(f"[Patcher] Scanning binary infrastructure: {path}")
        with open(path, 'rb') as file:
            data = file.read()
            
        modified = False
        for original, internal_target in replacements.items():
            if original in data:
                # Pad to keep perfect binary offsets intact
                aligned_patch = internal_target.ljust(len(original), b'\x00')
                data = data.replace(original, aligned_patch)
                modified = True
                
        if modified:
            with open(path + ".bak", 'wb') as backup:
                backup.write(data)
            with open(path, 'wb') as output:
                output.write(data)
            print(f"[Patcher] Successfully hooked endpoints in: {path}")

if __name__ == '__main__':
    run_hex_patcher()
