import os
import shutil
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
from datetime import datetime

def setup_logger(log_file='./vectordb/log.txt'):
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def walk_and_process(src_dir, dest_dir, vectordb: FAISS):
    files_processed = 0
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(src_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            shutil.move(file_path, os.path.join(dest_dir, filename))
    logging.info(f"Total files processed: {files_processed}")

if __name__ == "__main__":
    try:
        setup_logger()
        logging.info(f"Starting updating index and knowledge_base")
        start_time = datetime.now()
        logging.info(f"Script started at {start_time}")
        embeddings = OllamaEmbeddings(model="all-minilm")
        vectordb = FAISS.load_local("./vectordb", embeddings, allow_dangerous_deserialization=True)
        source_directory = "./update_base"
        destination_directory = "./knowledge_base"
        glob_pattern = "**/*.txt"
        loader = DirectoryLoader(
            path=source_directory,
            glob=glob_pattern,
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        docs = loader.load()
        print(f"Update base are loaded, {len(docs)} documents")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # chunk size (characters)
            chunk_overlap=200,  # chunk overlap (characters)
            add_start_index=True,  # track index in original document
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
        all_splits = text_splitter.split_documents(docs)
        vectordb.add_documents(all_splits)
        vectordb.save_local("./vectordb")
        logging.info(f"Added new chunks: {len(all_splits)}, total chunks: {vectordb.index.ntotal}")
        logging.info(f"Finished updating index, starting cleanup")
        walk_and_process(source_directory, destination_directory, vectordb)
        end_time = datetime.now()
        logging.info(f"Script ended at {end_time}")
        logging.info(f"Duration: {(end_time - start_time)}")
    except Exception as e:
        logging.error(f"Error updating index and knowledge_base {e}")
