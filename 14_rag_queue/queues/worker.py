# worker orchestration for RAG Queue. A processor function that will be called by the worker to process the user query and return the response.
# The processor function will search for relevant chunks in the vector database based on the user query and then use the retrieved context to generate a response using the OpenAI API.
import json
from openai import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

with open('../tokens/tokens.json') as f:
    json_data = json.load(f)
    token = json_data['HF_TOKEN']

openai_client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=token,
    )

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vector_db = QdrantVectorStore.from_existing_collection(url='http://localhost:6333', collection_name='pdf_chunks',
                                                           embedding=embedding_model)

def process_query(query: str):
    print('searching for relevant chunks in the vector database based on the user query...')
    search_results = vector_db.similarity_search(query=query)

    context = "\n\n\n".join([f"Page Content: {result.page_content}\n Page Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
                                for result in search_results])

    SYSTEM_PROMPT = f"""You are a helpful assistant that answers user query based on the available context retrieved from a pdf document along with the page_content and page number. 
    If you don't know the answer based on the following information, say "I don't know".

    You should only answer the user based on the following context and navigate the user to the relevant page number in the pdf document if the answer is present in the context.

    Context: 
    {context}
    """

    response = openai_client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
    )

    return response.choices[0].message.content

