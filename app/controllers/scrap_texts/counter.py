import os

def counter(path):
    current_dir = os.path.dirname(__file__)
    texts_path = os.path.join(current_dir, "../..", "texts")
    spain_path = os.path.join(texts_path, "spain")
    global_path = os.path.join(texts_path, "global")
    
    spain_files = len(os.listdir(spain_path))
    global_files = len(os.listdir(global_path))
    
    return (spain_files, global_files)