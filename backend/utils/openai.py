from django.conf import settings
from openai import OpenAI

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
