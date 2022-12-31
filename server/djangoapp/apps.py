from django.apps import AppConfig

from dotenv import load_dotenv
import os

load_dotenv()


class DjangoappConfig(AppConfig):
    name = 'djangoapp'
    get_dealership_url = str(os.getenv('GET_DEALERSHIP_URL'))
    get_review_url = str(os.getenv('GET_REVIEW_URL'))
    post_review_url = str(os.getenv('POST_REVIEW_URL'))
    nlu_analyze_url = str(os.getenv('NLU_ANALYZE_URL'))
    nlu_analyze_api_key = str(os.getenv('NLU_ANALYZE_API_KEY'))
