from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Raised when the configured AI service cannot return a response."""


def generate_career_analysis(prompt):
    if not settings.GEMINI_API_KEY:
        raise AIServiceError('Gemini is not configured.')
    try:
        from google import genai

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )
        result = (interaction.output_text or '').strip()
        if not result:
            raise AIServiceError('Gemini returned an empty response.')
        return result
    except AIServiceError:
        raise
    except Exception as exc:
        logger.exception('Gemini request failed: %s', exc)
        raise AIServiceError('The AI service is temporarily unavailable.') from exc