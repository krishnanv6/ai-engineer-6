from gitsource import GithubRepositoryDataReader
import frontmatter

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
# for doc in documents:
    # print(f"Title: {doc.get('title', 'No Title')}, filename: {doc.get('filename')}")