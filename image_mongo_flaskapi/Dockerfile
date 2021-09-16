FROM python
ADD api.py requirements.txt ./
RUN apt update && apt install python3-pip -y && pip install -r requirements.txt
WORKDIR .
CMD python3 api.py
