# A studygo set to csv program
This program scrapes every link in links.txt and converts it into a csv file.
This can be useful to migrate from studygo to another flashcards program.

## Installation
```shell
pip install -r requirements.txt
# or 
python3 -m pip install -r requirements.txt
```

Put some url's from studygo lists on each line

**Example links.txt**
```text
https://studygo.com/nl/learn/lists/175020294/hoofdstuk-1f
https://studygo.com/nl/learn/lists/175020276/hoofdstuk-1d
```

Afterwards run *main.py* 
```shell
python3 main.py
# or
python main.py
```
