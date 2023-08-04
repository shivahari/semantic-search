from fastapi import FastAPI, responses
from semantic_search import FaissIdx

app = FastAPI()
faiss_obj = FaissIdx()
index = faiss_obj.get_index(index_name='Tags.index')
doc_map = faiss_obj.get_pickle(pickle_name='Tags.pickle')

@app.get("/sem-search/{word}")
async def sem_search(word):
    "Semantic search a word"
    response = faiss_obj.search_doc(query=word,
                                    index=index,
                                    doc_map=doc_map)
    return responses.JSONResponse(status_code=200,content=response)
