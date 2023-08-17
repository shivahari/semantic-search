from fastapi import FastAPI, responses
from semantic_search import FaissIdx

app = FastAPI()
faiss_obj = FaissIdx()
index = faiss_obj.get_index(index_name='Tags.index')
doc_map = faiss_obj.get_pickle(pickle_name='Tags.pickle')


@app.get("/sem-search/{word}")
async def sem_search(word: str) -> responses.JSONResponse:
    "Semantic search a word"
    response = faiss_obj.search_doc(query=word,
                                    index=index,
                                    doc_map=doc_map)
    return responses.JSONResponse(status_code=200,content=response)

@app.get("/sem-search-score/{word}")
async def sem_search_with_score(word: str) -> responses.JSONResponse:
    "Semantic search a word"
    response = faiss_obj.search_doc(query=word,
                                    index=index,
                                    doc_map=doc_map,
                                    k=10,
                                    return_scores=True)
    return responses.JSONResponse(status_code=200,content=response)
