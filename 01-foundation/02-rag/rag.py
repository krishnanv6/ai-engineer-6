import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import requests
import io
import zipfile
import frontmatter
from minsearch import Index

print(Path.cwd())
load_dotenv(r"C:\Users\v2kri\OneDrive\ai\Alex\from-rag-to-agents\ai-engineer-6\.env")

repo_owner='evidentlyai'
repo_name='docs'
branch_name='main'

zip_url = f"https://github.com/{repo_owner}/{repo_name}/archive/refs/heads/{branch_name}.zip"
zip_response= requests.get(zip_url)
if zip_response.status_code == 200:
    print(f"Successfully read the zip file from {zip_url}")
    zip_archive =zipfile.ZipFile(io.BytesIO(zip_response.content))
    filenames=zip_archive.namelist()
    print(filenames[20:30], end="")
    # print(zip_response.content)
    filename ='docs-main/docs/platform/alerts.mdx'
    mdx_filename = zip_archive.open(filename)
    mdx_content = mdx_filename.read().decode('utf-8')
    print("Sample Content----")
    print(mdx_content[:500], end="")
    post = frontmatter.loads(mdx_content)
    print(post.content[:100])
    print(post.metadata)
    title =post.metadata.get('title','No Title')
    description=post.metadata.get('description','No Description')
    print(f"Title: {title}")
    print(f"Description: {description}")
    
    _,filename_corrected=filename.split('/',maxsplit=1)
    print(filename_corrected)
    docs ={ "content":post.content,
            "title":post.metadata.get('title','No Title'),
            "description":post.metadata.get('description','No Description'),
            "filename":filename_corrected
    }
    # print(docs)
else:
    print(f"Failed to download the zip file from {zip_url}. Status code: {zip_response.status_code}")
    
def read_github_repository(repo_owner, repo_name, branch="main"):
    url = f"https://github.com/{repo_owner}/{repo_name}/archive/refs/heads/{branch}.zip"
    response=requests.get(url)
    response.raise_for_status()
    print(response.status_code)
    
    documents=[]
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        for file_path in zip_ref.namelist():
            if not file_path.endswith(('.md', '.mdx')):
                continue
            with zip_ref.open(file_path) as file:
                content = file.read().decode('utf-8')
                post = frontmatter.loads(content)
                doc={
                    'content':post.content,
                    'title':post.metadata.get('title'),
                    'description':post.metadata.get('description'),
                    'filename':file_path.split('/', maxsplit=1)[-1]
                }
                documents.append(doc)
    return documents

repo_owner = 'evidentlyai'
repo_name = 'docs'

documents = read_github_repository(repo_owner, repo_name)
print(f"downloaded documents {len(documents)}")

index = Index(
    text_fields=["content", "title", "description"],
    keyword_fields=["filename"]
)
index.fit(documents)

query ='LLM as a Judge'
results = index.search(query, num_results=5)
print(len(results))
