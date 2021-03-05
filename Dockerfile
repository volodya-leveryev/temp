FROM python:slim
WORKDIR /myapp
COPY . .
RUN pip install -r requirements.txt
CMD ['gunicorn', 'app:app']