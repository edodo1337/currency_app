FROM python:3.7

# ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r /code/requirements.txt
WORKDIR /code/backend
CMD ["python3", "main.py"]
EXPOSE 8000

