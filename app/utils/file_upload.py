import os
import secrets
from flask import current_app
from werkzeug.utils import secure_filename

def save_file(file, folder_name, max_size_mb=None):
    """
    Saves a file to the specified folder within static/uploads.
    Returns the filename if successful, None if size limit exceeded or no file.
    """
    if not file:
        return None
        
    # Enforce size limits (Section 6.2)
    if max_size_mb:
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > max_size_mb * 1024 * 1024:
            return None

    original_filename = secure_filename(file.filename)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(original_filename)
    filename = random_hex + f_ext
    
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
    os.makedirs(upload_path, exist_ok=True)
    
    file.save(os.path.join(upload_path, filename))
    return filename
