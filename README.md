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
* Extract poems
* Translate to English
* Vectorize the translation
* Create AAN index - FAISS index
* Search for similarities