# Pull the base docker image of python with tag 3.10.6
FROM python:3.10.6

WORKDIR /app

COPY ClothesReviewHub.py /app/

COPY requirements.txt /app/

COPY damg7245-team3-assignment5-b0ba9f72c8a3.json /app/

RUN pip install -r requirements.txt

COPY pages /app/pages

COPY Logging /app/Logging

COPY amazonWebScraper.py /app/

COPY ProductBuy.py /app/

EXPOSE 8501

CMD ["streamlit", "run", "ClothesReviewHub.py", "--server.port", "8501"]