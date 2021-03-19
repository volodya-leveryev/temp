FROM python:slim
WORKDIR /myapp
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "-b", "0.0.0.0", "fiit1:create_app()"]
