python
import os

def is_zip_file(filename):
    try:
        with open(filename, 'rb') as f:
            return f.read(4) == b'PK\x03\x04'
    except:
        return False

def get_file_size(filename):
    size = os.path.getsize(filename)
    
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size/1024:.1f} KB"
    else:
        return f"{size/(1024*1024):.1f} MB"
