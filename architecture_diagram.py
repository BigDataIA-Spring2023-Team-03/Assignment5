from diagrams import Diagram, Edge, Cluster, Node
from diagrams.onprem.client import User, Users
from diagrams.aws.storage import SimpleStorageServiceS3 as s3
from diagrams.custom import Custom

with Diagram("ASSIGNMENT-5", show=False, direction='LR'):
    user = Users("users")
    user2 = User("user")
    imagefile = Custom("Image File", "./t-shirt.jpg")
    imagefile2 = Custom("Image File", "./t-shirt.jpg")
    datastorage = s3("AWS S3")

    with Cluster("Application Instance"):

        with Cluster("Services"):
            cloudapi = Custom("Google Cloud Vision", "./gcpapi.png")
            serpapi = Custom("SerpAPI", "./serpapi.png")  
            chatgpt = Custom("Chat GPT", "./chatgpt.png")
            deepai = Custom("Deep AI", "./deepai.png")      

        with Cluster("Applications"):
            userfacing = Custom("Streamlit", "./streamlit.png")

        # with Cluster("Batch Processing"):
        #     airflow = Airflow("Airflow") 
        #     whisper = Custom("Whisper", "./whisper.jpg")      
             
    
    # Defining Edges
    user >> Edge(label = "Click Picture") >> imagefile
    user >> Edge(label = "Login to Dashboard") >> userfacing
    user >> Edge(label = "Uploads Image") >> userfacing
  
    userfacing << Edge(label = "\n\n\n\n\n\n\nStores Image on S3 if does not exist") << datastorage
    userfacing >> Edge(label = "Upload Image from S3") >> datastorage
    
    userfacing >> Edge(label = "Image Recognition and Classification") >> cloudapi
    cloudapi >> Edge(label = "Logo & Labels") >> serpapi
    serpapi >> Edge(label = "Similar Items and \ntheir Reviews") >> chatgpt
    chatgpt >> Edge(label = "Purchase Suggestion") >> user2
    chatgpt >> Edge(label = "Compares Images") >> deepai 

    deepai >> Edge(label = "Provide Best Matched Result") >> imagefile2

    