from google import genai

# The SDK reads GEMINI_API_KEY from the environment.
client = genai.Client()

# Send our first request to Gemma 4.
response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents=(
        "An online store changed its return policy "
        "from 14 days to 7 days. "
        "Explain the customer impact in one sentence."
    ),
)

print(response.text)