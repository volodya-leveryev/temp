FROM python:slim
WORKDIR /myapp
COPY . .
RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0", "fiit1:create_app()"]
