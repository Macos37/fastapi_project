FROM python:3.9
WORKDIR /
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt
COPY . /
ENV DATABASE_URL=sqlite:////app/test.db
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]