# Similarity Search on the Bhagavatham

### Setup

* Create Python3 virtual env and activate the env.
* Install the packages using requiremets.txt
* Install IndicTransTokenizer
    - git clone https://github.com/VarunGumma/IndicTransTokenizer
    - cd IndicTransTokenizer
    - pip install --editable ./
* Setup PYTHONPATH
   - export PYTHONPATH=$PYTHONPATH:\<root\>/bhagavatam/src

### Jobs
#### Extract poems
#### Translate to English
#### Vectorize the transaction
#### Create AAN index - FAISS index
#### Start the FAISS search service 
     uvicorn annservice:app --reload --port 8081
#### Search for smililarities
#### Start the streamlit app
    streamlit run similaritysearchchat.py