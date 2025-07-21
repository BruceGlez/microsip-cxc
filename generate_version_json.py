import hashlib
import json
import sys
import os

# Constants
EXE_FILENAME = "MicrosipTool.exe"
REPO = "bruceglez/microsip-actualizador"

def sha256sum(file_path):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def main(version):
    exe_path = os.path.join("dist", EXE_FILENAME)
    if not os.path.isfile(exe_path):
        print(f"ERROR: File not found: {exe_path}")
        sys.exit(1)

    sha256 = sha256sum(exe_path)

    version_data = {
        "version": version,
        "url": f"https://github.com/{REPO}/releases/download/v{version}/{EXE_FILENAME}",
        "sha256": sha256
    }

    with open("version.json", "w") as f:
        json.dump(version_data, f, indent=2)

    print("✅ version.json generated.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_version_json.py <version>")
        sys.exit(1)
    main(sys.argv[1])
