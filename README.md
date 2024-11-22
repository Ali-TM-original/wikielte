<h1 style="text-align:center;">WIKIELTE</h1>
<p style="text-align:center;">Discord bot to store user resources in a secure database</p>

# Running
To run the bot on Production just use docker 🙏
```commandline
docker build -t <image_name> .
----------------------------------------------
docker run <image_name>
```
To run for production
--
make sure you have python 3.11 setup on your machine and you use proper commands for your OS
```commandline
-- windows
    pip install -r ./REQUIREMENTS.txt
    python ./main.py
-- linux
    pip3 install -r ./REQUIREMENTS.txt
    python3 ./main.py
```