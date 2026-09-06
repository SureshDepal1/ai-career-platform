from google import genai
from django.conf import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def generate_career_analysis(prompt):
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )

    return interaction.output_text