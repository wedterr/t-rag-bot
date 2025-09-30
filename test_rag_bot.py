from main import LoggerLLM, init_chain, init_vectordb, semantic_vectordb_search

with open('golden_questions.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    logger = LoggerLLM(key_words=['важно', 'точно', 'ответ'])
    vectordb = init_vectordb()
    chain = init_chain()
    for line in lines:
        query = line.strip()
        docs, query_context, cleaned_query, bad_query = semantic_vectordb_search(query, vectordb)
        response = chain.invoke({"input": cleaned_query, "context": query_context})
        chunks_found = len(query_context) > 0
        logger.log_request(query, response, chunks_found, [f'{doc.metadata["source"]}:{doc.metadata["start_index"]}' for doc in docs])