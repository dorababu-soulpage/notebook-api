FROM python:3.7.5

WORKDIR /apps

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

COPY styles/custom.css /usr/local/lib/python3.7/site-packages/notebook/static/custom/


EXPOSE 9000

CMD ["python", "main.py"]