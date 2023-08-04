# A semantic search app #
A semantic search app using Faiss

## Setup environment: ##
1. Create a `venv`
2. Run `python -m pip install -r requirements.txt`

## How to run app? ##
1. Add a XML dataset file, the name of the XML file is set as `Tags.xml` in the app.
2. Run `python semantic-search.py` command to create a Faiss index from the XML dataset file and save the index to current directory, pass a tech as input to validate index creation, run `exit` to exit the `semantic-search` app.
3. Start the FastAPI app - `uvicorn fastapi_app:app`
4. Start the Flask app - `python flask_app.py`
5. Navigate to `http://127.0.0.1:5000/` in a browser
6. Enter a tech in the `Tech` text box and find the relavent results returned from the dataset
