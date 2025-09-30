import time
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def test_search(vectordb):
    test_queries = [
        "Who is Xarn Velgor?",
        "What is Synth Flux?",
        "What is Void Core?",
        "Who was Dwarfs?",
        "Where was Shrubrews?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = vectordb.similarity_search(query, k=3)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.metadata['source']}")
            print(f"{result.page_content[:100]}...\n")

directory_path = "./knowledge_base"
glob_pattern = "**/*.txt"
loader = DirectoryLoader(
    path=directory_path,
    glob=glob_pattern,
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)

docs = loader.load()
print(f"Knowledge base are loaded, {len(docs)} documents")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # chunk size (characters)
    chunk_overlap=200,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
    separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
)
start_time = time.time()
all_splits = text_splitter.split_documents(docs)
embeddings = OllamaEmbeddings(model="all-minilm")
vectordb = FAISS.from_documents(all_splits, embeddings)
processing_time = time.time() - start_time
print("FAISS vectordb created",len(docs))
test_search(vectordb)
vectordb.save_local("./vectordb")
print(f"FAISS vectordb saved, {len(docs)} documents")
print(f"Number of chunks: {len(all_splits)}")
print(f"Processing time: {processing_time:.2f} seconds")
