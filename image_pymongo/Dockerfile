FROM python
ADD collection_wine_test.py requirements.txt winemag-data-130k-v2.json ./
RUN apt update && apt install python3-pip -y && pip install -r requirements.txt
WORKDIR .
CMD python3 collection_wine_test.py
