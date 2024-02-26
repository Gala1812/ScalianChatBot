from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.schema import Document


class TextLoader:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load(self):
        documents = []
        for root, _, files in os.walk(self.folder_path):
            for filename in files:
                if filename.endswith(".txt"):
                    file_path = os.path.join(root, filename)
                    with open(file_path, "r", encoding="utf-8") as file:
                        lines = file.readlines()
                        if len(lines) >= 3:
                            title = lines[0].strip()
                            url = lines[1].strip()
                            text = "".join(lines[2:]).strip()
                            metadata = {
                                "title": title,
                                "url": url,
                                "filename": filename,
                            }
                            documents.append(
                                Document(page_content=text, metadata=metadata)
                            )
                        else:
                            print(f"Archivo {filename} no tiene suficientes líneas.")

        return documents


def load_documents(file_path: str):
    loader = TextLoader(file_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1600, length_function=len, chunk_overlap=160
    )

    return text_splitter.split_documents(data)
