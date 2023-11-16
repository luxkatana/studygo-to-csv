# A studygo set to csv program
This program scrapes every link in links.txt and converts it into a csv file.
This can be useful to migrate from studygo to another flashcards program.

## Installation
```shell
pip install -r requirements.txt
# or 
python3 -m pip install -r requirements.txt
```

You'll need a chromedriver.exe for selenium. To install one: 
<ol>
<li>Head to https://chromedriver.chromium.org/downloads</li>
<li>and download a chromedriver based on your google chrome's version  and your OS</li>
<li>Unzip the downloaded zip from the website</li>
<li>Move the <strong>chromedriver.exe</strong> to this project's folder</li>
</ol>

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

## Configuration
modify **config.toml** to change the behaviour of the program

> If your OS is unix-based, you'll need to change the chromedriver path in config.toml to ./chromedriver

> It is recommended to manually specify chrome_path on unix-based operating systems