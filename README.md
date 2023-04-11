# Assignment5
ClothesReviewHub

Initial Presentation: https://docs.google.com/presentation/d/1xieFRIxBQXawJvA3IkaHfDNMV2Xv3c68HzXHwrevpMo/edit#slide=id.g209c36e65e3_2_227

Google Colab: https://codelabs-preview.appspot.com/?file_id=1mMz2OG9YK_P8xhHtDFceut6i6YMmXcHIEY_TfnvP36k#0

# Live Application Link
[http://44.214.57.19:8501](http://44.214.57.19:8501)

# CodeLab Documentation
https://codelabs-preview.appspot.com/?file_id=1mMz2OG9YK_P8xhHtDFceut6i6YMmXcHIEY_TfnvP36k#0

# Overview - Clothing Review Hub
See some clothes you like and want to buy it or something similar for yourself? Take a picture and get links to vendors and a summary of reviews to see if it's a worthwhile purchase.

## Moto:
Where can I buy that?

## Business Problems:
Nowadays it's a lot easier to find information on a product of clothing based on a picture, but it still takes a fair amount of manual input to find the exact product. This app would speed up that process.
When you're shopping online reviews are key, but it's a real pain combing through all the reviews and trying to decide the key points to consider. This app will do that for you and provide a quick clear summary of user reviews.

# Components
## Streamlit - streamlit/ in the root path
Used Python Streamlit for the frontend of our application. The user has 3 options for image upload; select a file from S3, take a picture, or upload a file. The UI is then populated with the top 3 results from Walmart after searching for the logo and labels generated from the Cloud Vision API.

### Page Layout:
- **ClothesReviewHub** - We can select a file/upload a file/click an image from the Camera Image Page. It gives the similar results based on the image uploaded and also summarizes the reviews from Walmart website. <br>
- **Camera Image** - User can use this page to click an image of an outfit and label the image, it will be uploaded to S3 bucket as well. <br>
- **Analytics Dashboard** - This dashboard records different usage statistics for the app.
     Access is granted via a password known by the admins

## APIs
### Google Cloud Vision API
To generate Label and Logo list from an image that the user uploaded.
### Chat Completion OpenAI API
To summarize the reviews which we got for the top 3 relevant orders.

## Docker
Streamlit has been dockerized.

Dockerfile for the streamlit
```
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
```

There are docker-compose files for both streamlit and airflow in their respective directories.

Docker Compose file for streamlit application
```
version: "3"
services:
  app:
    env_file:
      - .env
    container_name: clothesreviewhub
    build:
      dockerfile: Dockerfile
    command: "streamlit run --server.port 8501 --server.enableCORS false ClothesReviewHub.py"
    ports:
      - "8501:8501"
    image: clothesreviewhub:v1
```

# Running Locally
Steps to install and run the application locally:
- Make sure to install the prerequisites - Docker Desktop, Git
  -- Clone the repository
```
git clone https://github.com/BigDataIA-Spring2023-Team-03/Assignment4.git 
```

- Change the directory to streamlit
```
cd streamlit
```
- Create virtual environment
```
python -m venv streamlit_venv
```

- Docker build and up
```
docker-compose build
docker-compose up
```

This will start the streamlit application in the port 8501
> http://localhost:8501/

This will start the airflow in the port 8080
> http://localhost:8080/

# Architecture Diagram
![Arch Diagram](https://user-images.githubusercontent.com/91744801/230576197-35a62a95-bed5-493a-81bf-ce0d9b7887f2.png)

# Attestation
WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT
AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK. <br>

Contribution:
- Raj Mehta: 25%
- Mani Deepak Reddy Aila: 25%
- Jared Videlefsky: 30%
- Rumi Jha: 20%
