from os import scandir, rename
from os.path import exists, join, splitext
from shutil import move
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Directories add your directories locations
source_dir = ""
dest_dir_sfx = ""
dest_dir_music = ""
dest_dir_video = ""
dest_dir_image = ""
dest_dir_documents = ""
dest_dir_work_files = ""

# Supported file types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
work_file_extensions = [".py", ".ipynb", ".html", ".css", ".zip"]

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry.path, dest)
    logging.info(f"Moved file: {name} to {dest}")

def on_cleaner():
    with scandir(source_dir) as entries:
        for entry in entries:
            if entry.is_file():
                name = entry.name
                check_audio_files(entry, name)
                check_video_files(entry, name)
                check_image_files(entry, name)
                check_document_files(entry, name)
                check_work_files(entry, name)

def check_audio_files(entry, name):
    for audio_extension in audio_extensions:
        if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
            if entry.stat().st_size < 10_000_000 or "SFX" in name:
                dest = dest_dir_sfx
            else:
                dest = dest_dir_music
            move_file(dest, entry, name)
            break

def check_video_files(entry, name):
    for video_extension in video_extensions:
        if name.endswith(video_extension) or name.endswith(video_extension.upper()):
            move_file(dest_dir_video, entry, name)
            break

def check_image_files(entry, name):
    for image_extension in image_extensions:
        if name.endswith(image_extension) or name.endswith(image_extension.upper()):
            move_file(dest_dir_image, entry, name)
            break

def check_document_files(entry, name):
    for documents_extension in document_extensions:
        if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
            move_file(dest_dir_documents, entry, name)
            break

def check_work_files(entry, name):
    for work_file_extension in work_file_extensions:
        if name.endswith(work_file_extension) or name.endswith(work_file_extension.upper()):
            move_file(dest_dir_work_files, entry, name)
            break

if __name__ == "__main__":
    on_cleaner()
