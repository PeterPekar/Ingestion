# import basics
import os
from dotenv import load_dotenv

# import langchain
from langchain.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings

# import supabase
from supabase.client import Client, create_client

# load environment variables
load_dotenv()  

# initiate supabase db
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# initiate embeddings model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# load pdf docs from folder 'documents'
loader = UnstructuredFileLoader("documents/LASAL Text_eng.docx")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# store chunks in vector store
vector_store = SupabaseVectorStore.from_documents(
    docs,
    embeddings,
    client=supabase,
    table_name="documents2",
    query_name="match_documents2",
    chunk_size=1000,
)