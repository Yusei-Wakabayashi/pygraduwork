FROM python:3.8

WORKDIR /app

# requirements だけコピー（キャッシュ効く）
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]
