#def main():
#    print("Hello from class-2!")


#if __name__ == "__main__":
#    main()
from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="天空為什麼是藍的？"
)
print(response.text)

