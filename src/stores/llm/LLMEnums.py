from enum import Enum

class LLMType(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"

class OpenAIEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
class CoHereEnum(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"

    DOCUMENT = "search_document"
    QUERY = "search_query"

class DocumentType(Enum):
    DOCUMENT = "document"
    QUERY = "query"
