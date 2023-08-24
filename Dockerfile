FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

# Run main.py when the container launches
CMD ["python", "main.py"]
