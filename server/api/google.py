from google import genai
from PIL import Image

client = genai.Client(api_key="YOUR_API_KEY")

image = Image.open("/path/to/organ.png")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=[image, "Tell me about this instrument"]
)
print(response.text)