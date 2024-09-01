import ui_constants as UC
from vertexai.generative_models import HarmCategory, HarmBlockThreshold, SafetySetting


GC_PROJECT_NAME = 'arvato-developments'
LOCATION = 'asia-southeast1'

GEMINI_HYDE_MODEL = 'gemini-1.5-pro'
GEMINI_EMBEDDING_EN = 'text-embedding-004' # 英語のみの対応
GEMINI_EMBEDDING_MULTI = 'text-multilingual-embedding-002'
GEMINI_QA_MODEL = 'gemini-1.5-pro'
# GEMINI_RERANK_MODEL = 'gemini-1.5-pro-exp-0801'


K = 4

# データファイルのパス設定
FAISS_FILES = {
    UC.JAPANESE: "./knowledge_data/JA_08_02_2024_V3.faiss",
    UC.SPANISH: "./knowledge_data/ES_08_07_2024.faiss",
    UC.INDONESIAN: "./knowledge_data/ID_08_12_2024.faiss",
    UC.KOREAN: "./knowledge_data/KO_08_12_2024.faiss",
    UC.VIETNAMESE: "./knowledge_data/VI_08_14_2024.faiss",
    UC.THAI: "./knowledge_data/TH_08_19_2024.faiss",
    UC.ENGLISH: "./knowledge_data/EN_08_07_2024.faiss"
}

JSON_FILES = {
    UC.JAPANESE: "./knowledge_data/JA_08_02_2024_V3.json",
    UC.SPANISH: "./knowledge_data/ES_08_07_2024.json",
    UC.INDONESIAN: "./knowledge_data/ID_08_12_2024.json",
    UC.KOREAN: "./knowledge_data/KO_08_12_2024.json",
    UC.VIETNAMESE: "./knowledge_data/VI_08_14_2024.json",
    UC.THAI: "./knowledge_data/TH_08_19_2024.json",
    UC.ENGLISH: "./knowledge_data/EN_08_07_2024.json"
}

GENERATION_CONFIG = {"temperature": 0.8}

SAFTY_SETTINGS = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        method=SafetySetting.HarmBlockMethod.SEVERITY,
        threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        method=SafetySetting.HarmBlockMethod.SEVERITY,
        threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        method=SafetySetting.HarmBlockMethod.SEVERITY,
        threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        method=SafetySetting.HarmBlockMethod.SEVERITY,
        threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
]

