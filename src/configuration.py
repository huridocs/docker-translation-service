import logging
import os
from pathlib import Path

import graypy

SRC_PATH = Path(__file__).parent.absolute()
ROOT_PATH = Path(__file__).parent.parent.absolute()
TRANSLATIONS_PORT = 11434
LANGUAGES_SHORT = ["en", "fr", "es", "ru", "ar", "sp"]
LANGUAGES = ["English", "French", "Spanish", "Russian", "Arabic", "Spanish"]

QUEUES_NAMES = os.environ.get("QUEUES_NAMES", "translations development_translations")

GRAYLOG_IP = os.environ.get("GRAYLOG_IP")
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
MODEL = os.environ.get("MODEL", "aya:35b")
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")

handlers = [logging.StreamHandler()]

if GRAYLOG_IP:
    handlers.append(graypy.GELFUDPHandler(GRAYLOG_IP, 12201, localname="translations_service"))

logging.root.handlers = []
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=handlers)
service_logger = logging.getLogger(__name__)

if LOGGING_LEVEL == "WARNING":
    service_logger.setLevel(logging.WARNING)
else:
    service_logger.setLevel(logging.INFO)



PROMPTS = {
    "Prompt 1": "Translate the below text to {language_to_name}, keep the layout, do not skip any text, do not output anything else besides translation:",
    "Prompt 2": """Please translate the following text into {language_to_name}. Follow these guidelines:  
      1. Maintain the original layout and formatting.  
      2. Translate all text accurately without omitting any part of the content.  
      3. Preserve the tone and style of the original text.  
      4. Do not include any additional comments, notes, or explanations in the output; provide only the translated text.  

Here is the text to be translated:  """,
    "Prompt 3": """Please translate the following text into {language_to_name}. Follow these guidelines:
1. Maintain the original layout and formatting.
2. Translate all text accurately without omitting any part of the content.
3. Preserve the tone and style of the original text.
4. Do not include any additional comments, notes, or explanations in the output; provide only the translated text.
5. Only translate the text between ``` and ```. Do not output any other text or character.

Here is the text to be translated:

```
{text_to_translate}
```
""",
    "Prompt 4": """Please translate only the text marked as "TARGET SEGMENT" into {language_to_name}. Use the "PREVIOUS SEGMENT" and "NEXT SEGMENT" only as context to help you understand the meaning, but do not translate them. 

Guidelines:
1. Maintain the original layout and formatting of the TARGET SEGMENT.
2. Translate all text in the TARGET SEGMENT accurately without omitting any part of the content.
3. Preserve the tone and style of the TARGET SEGMENT.
4. Do not include any additional comments, notes, or explanations in the output; provide only the translated TARGET SEGMENT.
5. The "PREVIOUS SEGMENT" and "NEXT SEGMENT" are provided only for context and may be `[empty]`.

Context:
PREVIOUS SEGMENT:
```
{previous_text}
```

TARGET SEGMENT (translate only this part):
```
{text_to_translate}
```

NEXT SEGMENT:
```
{next_text}
```
""",
    "Prompt 5": """

Please translate the following text into {language_to_name}. The text is an excerpt from a document with the following title:

{document_title}


Follow these guidelines:

1. Maintain the original layout and formatting.
2. Translate all text accurately without omitting any part of the content.
3. Preserve the tone and style of the original text.
4. Do not include any additional comments, notes, or explanations in the output; provide only the translated text.
5. Only translate the text between ``` and ```. Do not output any other text or character.

Here is the text to be translated:

```
{text_to_translate}
```

""",
}
