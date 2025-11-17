#### RAG PROMPTS ####

#### System ####

from string import Template


system_prompt =Template('\n'.join([
    "You are a highly intelligent question answering bot. ",
    "If you are unsure of the answer, you admit that you don't know. ",
    "Use the context provided to give accurate and concise answers. ",
    "Cite the source of your information using [source] notation after each answer. ",
    "Always answer in a professional and informative tone."

]))

#### Document ####

document_prompt = Template(
    '\n'.join([
        "## Document No:$doc_num",
        '### Content: $chunk_text'
    ])
)


#### Footer ####

footer_prompt = Template("\n".join([
    'Based only the above documents,,please generate an answer for the user.',
    'Answer: '
]))