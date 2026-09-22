FROM ml-base-cpu:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "demo.py", "--source", "data/test_1_office.jpg", "--output", "data/output_1.jpg", "--headless"]
