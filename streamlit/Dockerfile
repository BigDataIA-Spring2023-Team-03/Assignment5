# Pull the base docker image of python with tag 3.10.6
FROM python:3.10.6

# Change the working dir inside the container - cd /app
WORKDIR /app

# Copy main.py as source cod and req.txt as dependency
COPY ClothesReviewHub.py /app/

# avoid re-running the install step on every code change:
COPY requirements.txt /app/
COPY damg7245-team3-assignment5-b0ba9f72c8a3.json /app/
# Install the dependency
RUN pip install -r requirements.txt

COPY pages /app/pages

COPY Logging /app/Logging

COPY amazonWebScraper.py /app/
COPY ProductBuy.py /app/

### Container Env same as local at this point
EXPOSE 8501

CMD ["streamlit", "run", "ClothesReviewHub.py", "--server.port", "8501"]