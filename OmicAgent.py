import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from langchain_community.llms import Ollama

# Streamlit Layout Configuration
st.set_page_config(layout="wide")

# Sidebar
st.sidebar.header("🌍 Language Selection")
language = st.sidebar.selectbox("Choose response language:", ["English", "Telugu", "Tamil"])

st.sidebar.header("📊 Analytics Flags")
show_categorical_analysis = st.sidebar.checkbox("Show Categorical Column Analysis")
show_sample_data = st.sidebar.checkbox("Show Sample Data")
show_receptor_status = st.sidebar.checkbox("Show Receptor Status Distribution")
show_survival_analysis = st.sidebar.checkbox("Show Survival Analysis")
show_gene_expression = st.sidebar.checkbox("Show Gene Expression Insights")
show_correlation_heatmap = st.sidebar.checkbox("Show Correlation Heatmap")

st.sidebar.header("🎤 Voice Input")
voice_enabled = st.sidebar.checkbox("Enable Voice Input")

# Chatbot Title
st.markdown("<h1 style='text-align: center;'>🔬 AI-Driven Multi-Omics Data Analysis & Bot 🤖</h1>", unsafe_allow_html=True)

# Load Multi-Omics Dataset
file_path = "brca_data_w_subtypes.csv"
try:
    df = pd.read_csv(file_path)
    st.sidebar.success("Dataset loaded successfully!")
except FileNotFoundError:
    st.sidebar.error(f"File not found at path: {file_path}. Please verify the file location.")
    st.stop()

# Display Sample Data
if show_sample_data:
    st.subheader("Sample Data")
    st.dataframe(df.head())

# Categorical Column Analysis
if show_categorical_analysis:
    st.subheader("Categorical Column Analysis")
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_columns:
        st.write(f"Value counts for `{col}`:")
        value_counts = df[col].value_counts()
        st.write(value_counts)
        st.write("\n")

# Receptor Status Distribution
if show_receptor_status:
    st.subheader("Receptor Status Distribution")
    receptor_status = {
        "ER Status": df['ER.Status'].value_counts().to_dict(),
        "PR Status": df['PR.Status'].value_counts().to_dict(),
        "HER2 Status": df['HER2.Final.Status'].value_counts().to_dict()
    }
    st.write("Receptor Status Distribution:")
    st.json(receptor_status)

# Survival Analysis
if show_survival_analysis:
    st.subheader("Survival Analysis by Histological Type")
    survival_by_histology = df.groupby('histological.type')['vital.status'].value_counts().unstack(fill_value=0)
    st.bar_chart(survival_by_histology)

# Gene Expression Insights
if show_gene_expression:
    st.subheader("Gene Expression Insights")
    gene_columns = [col for col in df.columns if col.startswith("rs_")]
    gene_summary = df[gene_columns].describe()
    st.write("Summary Statistics for Key Genes:")
    st.dataframe(gene_summary)

# Correlation Heatmap
if show_correlation_heatmap:
    st.subheader("Correlation Heatmap")
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    correlation_matrix = df[numerical_columns].corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=False, cmap="coolwarm", cbar=True)
    st.pyplot(plt)

# Initialize Ollama Model
ollama_model = Ollama(model="wizardlm2:7b")  # Use the appropriate Ollama model

# Define Prompt Template for Multi-Omics Queries
def get_prompt(query):
    return f"""
You are an AI-driven multi-omics expert designed to answer questions about genomics, transcriptomics, proteomics, metabolomics, and other omics levels. Your goal is to provide accurate and concise responses based on your training data.
#### Context:
Multi-omics refers to the integration of multiple types of molecular information, such as the genome, epigenome, transcriptome, and proteome, to gain a deeper understanding of biological systems [[3]]. It enables the simultaneous analysis of multiple molecular compartments at high resolution [[4]].
#### Query:
{query}
#### Response Guidelines:
- Provide clear explanations of multi-omics concepts.
- If the query relates to applications, mention examples such as disease subtyping, biomarker discovery, or molecular mechanisms [[9]].
- Avoid fabricated or speculative information.
Answer:
"""

# Function to generate a greeting response
def generate_greeting_response():
    return "Hello! How can I assist you with multi-omics? 😊"

# Function to check if the query is a greeting
def is_greeting(query):
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "how are you", "what's up"]
    return any(greeting in query.lower() for greeting in greetings)

# Function to handle user queries
def handle_query(query):
    if is_greeting(query):
        return generate_greeting_response()
    else:
        # Check if the query is related to the dataset
        if "histological type" in query.lower():
            histological_types = df['histological.type'].value_counts()
            return f"Histological types in the dataset:\n{histological_types.to_string()}"
        elif "vital status" in query.lower():
            vital_status = df['vital.status'].value_counts()
            return f"Vital status distribution:\n{vital_status.to_string()}"
        elif "receptor status" in query.lower():
            receptor_status = {
                "ER Status": df['ER.Status'].value_counts().to_dict(),
                "PR Status": df['PR.Status'].value_counts().to_dict(),
                "HER2 Status": df['HER2.Final.Status'].value_counts().to_dict()
            }
            return f"Receptor status distribution:\n{receptor_status}"
        elif "gene expression" in query.lower():
            gene_columns = [col for col in df.columns if col.startswith("rs_")]
            gene_summary = df[gene_columns].describe()
            return f"Summary statistics for key genes:\n{gene_summary.to_string()}"
        else:
            # Use Ollama model for general multi-omics queries
            prompt = get_prompt(query)
            response = ollama_model.invoke(prompt)
            return response

# Chat Section
st.markdown("""
    <style>
        .chat-container {
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            height: 400px;
            overflow-y: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize chat history if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat Input (Text or Voice)
query = ""
if voice_enabled:
    audio_bytes = audio_recorder("Record your question", recording_color="#ff4d4d", neutral_color="#6699ff")
    if audio_bytes:
        with open("audio_query.wav", "wb") as f:
            f.write(audio_bytes)
        recognizer = sr.Recognizer()
        with sr.AudioFile("audio_query.wav") as source:
            audio_data = recognizer.record(source)
        try:
            query = recognizer.recognize_google(audio_data)
            st.success("Query: " + query)
        except:
            st.error("Could not recognize audio.")
else:
    query = st.chat_input("Enter your message here...")

# Process Query
if query:
    with st.spinner("Generating response..."):
        response = handle_query(query)
        if response:
            if language == "Telugu":
                response = GoogleTranslator(source="auto", target="te").translate(response)
            elif language == "Tamil":
                response = GoogleTranslator(source="auto", target="ta").translate(response)
            
            # Append to Chat History
            st.session_state.chat_history.append((query, response))

    # Display chat history
    st.subheader("Chat History")
    for q, r in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(q)
        with st.chat_message("assistant"):
            st.write(r)