# use Alpine Linux
FROM python:3.11.4

WORKDIR /usr/src/wikielte

#COPY REQUIREMENTS.txt .
COPY . .

ENV TOKEN=MTMwNjU4NTc4NjIwMzc2NjgyNQ.GHhg3R.BtVzH9NML-JZk_8jiq8uOg-wkfvDMYVUZmfLwU
ENV OWNER=410452466631442443
ENV ERRORLOGS=1309118794777493608

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r ./REQUIREMENTS.txt || (echo "Failed to install dependencies" && cat ./requirements.txt && exit 1)
CMD ["python", "./main.py"]