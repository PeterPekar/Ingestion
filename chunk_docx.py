import os
from dotenv import load_dotenv
from unstructured.partition.docx import partition_docx
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import Client, create_client
import pickle

# Load environment variables
load_dotenv()

# Initiate Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Initiate embeddings model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Directory containing the DOCX files
docx_directory = "documents"

# --- 1. GET ELEMENTS ---
raw_docx_elements = []
for filename in os.listdir(docx_directory):
    if filename.endswith(".docx"):
        file_path = os.path.join(docx_directory, filename)
        raw_docx_elements.extend(partition_docx(filename=file_path,
                                                # Unstructured first finds bounding boxes of elements in the document and then extracts the text within those boxes.
                                                # In structured documents, tables and other elements are carefully positioned.
                                                # You can use this parameter to ignore headers and footers.
                                                infer_table_structure=True,
                                                # --- CHUNKING STRATEGY ---
                                                # https://unstructured-io.github.io/unstructured/core/chunking.html
                                                chunking_strategy="by_title",
                                                max_characters=4000,
                                                new_after_n_chars=3800,
                                                combine_text_under_n_chars=2000,
                                               ))

# --- 2. CREATE A DICTIONARY TO STORE THE ELEMENTS ---
elements_dict = {}
for e in raw_docx_elements:
    # Generate a unique ID for each element
    element_id = str(e.id)
    # Get the text of the element
    text = e.text
    # Get the metadata of the element
    metadata = e.metadata.to_dict()
    # Add the element to the dictionary
    elements_dict[element_id] = {"text": text, "metadata": metadata}

# --- 3. STORE THE ELEMENTS IN A PICKLE FILE ---
with open('elements.pkl', 'wb') as f:
    pickle.dump(elements_dict, f)

# --- 4. CATEGORIZE ELEMENTS ---
tables = []
texts = []
for element in raw_docx_elements:
    if "unstructured.documents.elements.Table" in str(type(element)):
        tables.append(str(element))
    elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
        texts.append(str(element))

# --- 5. ADD TO VECTOR DB ---
vector_store = SupabaseVectorStore.from_texts(
    texts,
    embeddings,
    client=supabase,
    table_name="documents3",
    query_name="match_documents3",
)

print("DOCX files chunked and stored in vector database.")
