from filelock import FileLock, Timeout
import os
import sys

LOCK_PATH = os.path.join(os.path.expanduser("~"), ".microsip_credito.lock")

def verificar_instancia_unica():
    lock = FileLock(LOCK_PATH + ".lock")
    try:
        lock.acquire(timeout=0.1)
        return lock
    except Timeout:
        return None
