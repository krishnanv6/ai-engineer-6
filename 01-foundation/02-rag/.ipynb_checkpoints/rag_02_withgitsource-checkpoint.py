from gitsource import GithubRepositoryDataReader
import frontmatter
from minsearch import Index
from gitsource import document_chunks

reader = GithubRepositoryDataReader(
    repo_owner="evidentlyai",
    repo_name='docs',
    allowed_extensions={"md", "mdx"},)

files=reader.read()
print(f"loaded {len(files)} documents")

document = files[10]
print(document.filename)
print(document.content[:500])

post = frontmatter.loads(document.content)
data = post.to_dict()
data['filename'] = document.filename

document.parse()
documents = [f.parse() for f in files]
# print(data)
print(documents)
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
print(len(document_chunks)
print(document_chunks[1])
