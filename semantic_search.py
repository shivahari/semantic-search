# reference https://deepnote.com/blog/semantic-search-using-faiss-and-mpnet
import faiss
from pathlib import Path
import pickle 
import torch
from transformers import AutoTokenizer, AutoModel
from bs4 import BeautifulSoup

class SemanticEmbedding:
    def __init__(self, model_name='sentence-transformers/all-mpnet-base-v2'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
    
    #Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def get_embedding(self, sentences):
        # Tokenize sentences
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        # Perform pooling
        sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])

        # Normalize embeddings
        sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings.detach().numpy()

class FaissIdx:
    def __init__(self, dim=768):
        self.dim = dim
        self.model = SemanticEmbedding()
        self.ctr = 0

    def create_index(self):
        "Create a new index"
        return faiss.IndexFlatIP(self.dim)

    def get_index(self, index_name):
        "Get the index"
        try:
            return faiss.read_index(index_name)
        except FileNotFoundError:
            raise(f"Unable to find {index_name}, does the file exist?")

    def get_pickle(self, pickle_name):
        "Get the local pickle file"
        try:
            with open(pickle_name, 'rb') as pickled_file:
                return pickle.load(pickled_file)
        except FileNotFoundError:
            raise(f"Unable to find {pickle_name}, does the file exist?")

    def add_doc(self,
                document_text,
                index,
                doc_map):
        "Add doc to index"
        index.add(self.model.get_embedding(document_text))
        doc_map[self.ctr] = document_text # store the original document text
        self.ctr += 1

    def add_doc_from_xml(self,
                         xml_local_file,
                         html_element_property,
                         index,
                         doc_map):
        "Add doc to index from local xml file"
        html_element_property = html_element_property.lower()
        with open(xml_local_file, 'r') as xmlfile:
            xml = xmlfile.readlines()
        xml = "".join(xml)

        soup = BeautifulSoup(xml, "html.parser")
        rows = soup.find_all('row')

        for row in rows:
            print(f"Addding {row} to index")
            self.add_doc(row[html_element_property], index, doc_map)

    def search_doc(self,
                   query,
                   index,
                   doc_map,
                   k=5,
                   return_scores=False):
        "Search through the index"
        D, I = index.search(self.model.get_embedding(query), k)
        if return_scores:
            return [{doc_map[idx]: str(score)} for idx, score in zip(I[0], D[0]) if idx in doc_map]
        else:
            return [doc_map[idx] for idx, score in zip(I[0], D[0]) if idx in doc_map]

    def save_index_and_pickle(self,
                              index,
                              index_name,
                              doc_map,
                              pickle_name):
        "Save the index and dataset pickle file to local"
        faiss.write_index(index, index_name)
        with open(pickle_name, 'wb') as tnf:
            pickle.dump(doc_map, tnf, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    faiss_obj = FaissIdx()
    index = faiss_obj.create_index()
    doc_map = dict()

    if not Path('Tags.index').is_file():
        faiss_obj.add_doc_from_xml(xml_local_file='Tags.xml',
                                   html_element_property='TagName',
                                   index=index,
                                   doc_map=doc_map)
    if not Path('Tags.pickle').is_file():
        faiss_obj.save_index_and_pickle(index=index,
                                        index_name='Tags.index',
                                        doc_map=doc_map,
                                        pickle_name='Tags.pickle')

    local_index = faiss_obj.get_index(index_name='Tags.index')
    local_doc_map = faiss_obj.get_pickle(pickle_name='Tags.pickle')


    while True:
        tech = input("\nEnter a tech: ")
        if tech == "exit":
            break
        if tech.strip() == "":
            continue
        output = faiss_obj.search_doc(query=tech,
                                      index=local_index,
                                      doc_map=local_doc_map,
                                      k=10)
        print(output)