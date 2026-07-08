import json

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings # not free, you need to add $5 to https://platform.openai.com/settings/organization/billing/overview to make it work. You can use gemini embedding model which is compatible with openAI API and it's free to use. You just need to create a google cloud account and enable the gemini API to get the API key.
# from langchain_google_genai import GoogleGenerativeAIEmbeddings #Current api key used here doesn't support embeddings. Supports Text generation and chat completion only. So, we will use openAI embedding model for now. You can use gemini embedding model if you have an api key that supports embeddings.
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore


#pdf path
pdf_path = "pdfs/javascript_tutorial.pdf"

# 1.load this file in python program. IT will give page wise content of the pdf in form of list. Each page will be one element in the list.
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()
# print(docs[24]) #test

# 2.Chunking: Now we have page wise content in the form of list. We will use langchain text splitter to split the content of each page into smaller chunks.
# This is because most of the language models have a limit on the number of tokens they can process in one go.
# So, we need to split the content into smaller chunks to make it easier for the model to understand and process it.]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(docs)


# 3. Create vector embedding for each chunk using the embedding model. We will use OpenAI's embedding model for this purpose.
# Embeddings are numerical representations of text that capture the semantic meaning of the text.
# They allow us to compare the similarity between different pieces of text and retrieve relevant information based on the user's query.
# This embedding model needs to create an embedding for chunks and store it in a vector database.
# We will use Qdrant as our vector database to store the embeddings and perform similarity search.
# So, we need langchain qdrant vector store to connect to qdrant and store the embeddings in it.
# with open('../tokens/tokens.json') as f:
#     json_data = json.load(f)
#     token = json_data['GEMINI_API_KEY']

# since openAI embedding model needs an openAI API Key but since it's not free, we can use gemini embedding model which is compatible with openAI API and it's free to use.
# You just need to create a google cloud account and enable the gemini API to get the API key.
# embedding_model = OpenAIEmbeddings(model="text-embedding-3-large", api_key=token) #add your open api token here

# embedding_model = GoogleGenerativeAIEmbeddings(
#     model="embedding-001",
#     google_api_key=token,
# )

# use hugging face embedding model which is free to use and doesn't require any api key. You can use any hugging face embedding model of your choice. Here we are using sentence-transformers/all-MiniLM-L6-v2 model which is a good general purpose embedding model.
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#4. Store these vector embeddings to the qdrant vector database. We will use langchain qdrant vector store to connect to qdrant and store the embeddings in it.
# It will create an embedding for each chunk and store it in qdrant vector database. You can query this database to retrieve relevant chunks based on the user's query.
# Also, it will create a collection named "pdf_chunks" in qdrant to store the embeddings. If the collection already exists, it will add the new embeddings to the existing collection.
# collections in qdrant are like tables in relational databases. They are used to store and organize the data in the vector database. Each collection can have multiple vectors (embeddings) and each vector can have multiple metadata fields associated with it.
# It can be seen at http://localhost:6333/collections/pdf_chunks after running this code.
vector_store = QdrantVectorStore.from_documents(documents=chunks, embedding=embedding_model, url="http://localhost:6333", collection_name="pdf_chunks") #add your qdrant url here
print('Indexing completed successfully!')