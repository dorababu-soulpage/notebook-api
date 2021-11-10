FROM python:3.7.5

WORKDIR /apps

COPY requirements.txt ./

RUN ls

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080


CMD ["python", "main.py"]