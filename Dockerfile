FROM python:3.10.4-bullseye
ENV PATH=/usr/local/bin:$PATH

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN python -c "import nltk; nltk.download('popular')"

COPY philter-ucsf /app/

CMD [ "gunicorn" , "serve:app", "--bind=0.0.0.0" ]

EXPOSE 8000
