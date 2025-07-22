import os
import json
import requests
import hashlib
from packaging import version

# Remote version info JSON (must contain: version, url, hash)
VERSION_JSON_URL = "https://raw.githubusercontent.com/BruceGlez/microsip-cxc/master/version.json"

# Destination filename
DEST_FILENAME = "MicrosipTool_new.exe"

def get_download_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def get_local_version():
    try:
        version_path = os.path.join(get_download_path(), "version.json")
        with open(version_path, "r") as f:
            data = json.load(f)
            return version.parse(data.get("version", "0.0.0"))
    except:
        return version.parse("0.0.0")

def get_remote_data():
    try:
        response = requests.get(VERSION_JSON_URL, timeout=5)
        if response.ok:
            return response.json()
    except:
        pass
    return {}

def download_file(url, dest_path):
    response = requests.get(url, stream=True, timeout=10)
    if not response.ok:
        raise Exception(f"Error downloading: {response.status_code}")
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)

def verify_file_hash(path, expected_hash):
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest().lower() == expected_hash.lower()

def actualizar_aplicacion(url, expected_hash):
    download_path = os.path.join(get_download_path(), DEST_FILENAME)
    print("⬇️ Descargando nueva versión...")
    download_file(url, download_path)

    print("🔐 Verificando integridad...")
    if verify_file_hash(download_path, expected_hash):
        print("✅ Actualización descargada y verificada correctamente.")
    else:
        os.remove(download_path)
        raise Exception("❌ Hash inválido. Archivo eliminado.")

if __name__ == "__main__":
    local_ver = get_local_version()
    remote_data = get_remote_data()

    remote_ver = version.parse(remote_data.get("version", "0.0.0"))
    url_remoto = remote_data.get("url", "")
    hash_remoto = remote_data.get("hash", "")

    print(f"📦 Versión local: {local_ver}")
    print(f"🌐 Versión remota: {remote_ver}")

    if remote_ver > local_ver:
        actualizar_aplicacion(url_remoto, hash_remoto)
    else:
        print("✅ Ya tienes la última versión.")
