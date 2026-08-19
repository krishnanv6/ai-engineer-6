from gitsource import GithubRepositoryDataReader
import frontmatter
from minsearch import Index
from gitsource import chunk_documents
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(r"C:\Users\v2kri\OneDrive\ai\Alex\from-rag-to-agents\ai-engineer-6\.env")
import json

reader = GithubRepositoryDataReader(
    repo_owner="evidentlyai",
    repo_name='docs',
    allowed_extensions={"md", "mdx"},)

files=reader.read()
print(f"loaded {len(files)} documents")

document = files[10]
print(document.filename)
# print(document.content[:500])

post = frontmatter.loads(document.content)
data = post.to_dict()
data['filename'] = document.filename

document.parse()
documents = [f.parse() for f in files]
# print(data)
# print(documents)
enumerate_documents = list(enumerate(documents))

# print(enumerate_documents[10])
print(enumerate_documents[10][1]['title'])


index = Index(
    text_fields=["content", "title", "description"],
    keyword_fields=["filename"]
)
index.fit(documents)

query = "LLM as a Judge"
search_results = index.search(query, num_results=5)
print(f"number of search results: {len(search_results)}")

document_chunks=chunk_documents(documents)
print(len(document_chunks))
# print(document_chunks[1])`     `
chunk_index=Index(
    text_fields=["title","description","content"],
    keyword_fields=["filename"]
)
chunk_index.fit(document_chunks)
chunk_results=chunk_index.search(query)
openai_client = OpenAI()

def search(query):
    return chunk_index.search(query, num_results=5)

instructions = """
You're a course assistant, your task is to answer the QUESTION from the
course students using the provided CONTEXT
"""

def build_prompt(query, search_results):
    search_result_json = json.dumps(search_results, indent=2)

    user_prompt = f"""
    <QUESTION>
    {query}
    </QUESTION>

    <CONTEXT>
    {search_result_json}
    </CONTEXT>
    """.strip()

    return user_prompt

def llm(user_prompt, instructions=None,model='gpt-4o-mini'):
    messages=[]
    if instructions is not None:
        messages.append({
            "role":"system",
            "content":instructions
        })

    messages.append({
    "role":"user",
    "content": user_prompt
    })

    response = openai_client.responses.create(
        model=model,
        input=messages)
    
    return response.output_text


def rag(query):
    print("Running RAG for query:", query)
    search_results = search(query)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt, instructions=instructions)
    return answer

answer = rag('how do I implement llm as a judge?')
print("Answer from RAG:")
print(answer)