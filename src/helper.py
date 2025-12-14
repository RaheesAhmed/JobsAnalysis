import fitz # PyMuPDF
import os 
from dotenv import load_dotenv
from openai import OpenAI
from apify_client import ApifyClient



load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.
    
    Args:
        uploaded_file (str): The path to the PDF file.
        
    Returns:
        str: The extracted text.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    # Iterate through each page in the cv and extract text
    for page in doc:
        text += page.get_text()
    return text


# Function to interact with OpenAI API 
def ask_openai(prompt, max_tokens=500):
    """
    Sends a prompt to the OpenAI API and returns the response.
    
    Args:
        prompt (str): The prompt to send to the OpenAI API.
        model (str): The model to use for the request.
        temperature (float): The temperature for the response.
        
    Returns:
        str: The response from the OpenAI API.
    """
    
# Create a chat completion request
    response = client.chat.completions.create(
        model= "gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=max_tokens
    )
    # Return the response from the OpenAI API response
    return response.choices[0].message.content



