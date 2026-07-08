import json

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_db = QdrantVectorStore.from_existing_collection(url='http://localhost:6333', collection_name='pdf_chunks', embedding=embedding_model)

# Take user input
user_query = input("Enter query: ")

# do similarity search and get relevant chunks from the vector database based on the user's query. It will return a list of relevant chunks that are similar to the user's query.
# The similarity search is performed using the cosine similarity between the query embedding and the embeddings stored in the vector database.
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([f"Page Content: {result.page_content}\n Page Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
                         for result in search_results])

SYSTEM_PROMPT = f"""You are a helpful assistant that answers user query based on the available context retrieved from a pdf document along with the page_content and page number. 
If you don't know the answer based on the following information, say "I don't know".

You should only answer the user based on the following context and navigate the user to the relevant page number in the pdf document if the answer is present in the context.

Context: 
{context}
"""

with open('../tokens/tokens.json') as f:
    json_data = json.load(f)
    token = json_data['HF_TOKEN']


client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=token,
)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b:cerebras",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ],
)

print(f"🤖: {response.choices[0].message.content}")