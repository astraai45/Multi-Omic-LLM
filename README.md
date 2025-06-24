# Multi-Omic-LLM

Sure! Here's a template for the `README.md` file that you can use for your GitHub project. It includes an overview of the project, installation instructions, usage, and contributor information.

---

# Multi-Omics Cancer Data Analysis & AI-Driven Chatbot

## Overview

This project provides a comprehensive tool for the analysis of multi-omics cancer data, including genomics, transcriptomics, proteomics, and metabolomics. It leverages a conversational AI chatbot that allows users to interact with cancer-related datasets and perform various analyses such as receptor status distribution, survival analysis, gene expression insights, and more. Users can interact with the system using text input or voice commands.

The system uses the **Ollama** language model and integrates various Python libraries such as **Streamlit**, **Pandas**, **Matplotlib**, and **Seaborn** for data visualization and analysis.

## Features

* **Data Upload and Display**: Upload and display multi-omics datasets for analysis.
* **Categorical Column Analysis**: View the distribution of categorical data columns.
* **Receptor Status Distribution**: View distributions of receptor statuses like ER, PR, and HER2.
* **Survival Analysis**: Visualize survival data based on histological types.
* **Gene Expression Insights**: Get summary statistics for gene expression levels.
* **Correlation Heatmap**: Visualize correlations between different numerical columns.
* **AI Chatbot**: A conversational AI to assist with data analysis and provide insights based on user queries.
* **Voice Input**: Enable voice commands for interacting with the system (powered by Google Speech Recognition).

## Technologies Used

* **Streamlit** for web application development.
* **Pandas** for data manipulation and analysis.
* **Seaborn** & **Matplotlib** for data visualization.
* **Deep Translator** for language translation.
* **SpeechRecognition** for voice input functionality.
* **Langchain** with **Ollama** for AI-based responses to multi-omics queries.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<YOUR-USERNAME>/multi-omics-cancer-analysis.git
   cd multi-omics-cancer-analysis
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

5. Open the application in your browser by navigating to `http://localhost:8501`.

## Usage

1. **Load Dataset**: The system requires a multi-omics dataset in CSV format. By default, the dataset is expected to be named `brca_data_w_subtypes.csv`. Ensure your dataset has the required columns such as `histological.type`, `vital.status`, `ER.Status`, `PR.Status`, `HER2.Final.Status`, and gene expression data (e.g., columns starting with `rs_`).

2. **Voice Input**: You can enable voice input in the sidebar. Click the "Enable Voice Input" checkbox and use the voice recording feature to ask questions related to multi-omics data.

3. **AI Chatbot**: Enter your query in the chat input box, or use voice input to ask questions. The chatbot will provide responses based on the dataset and the AI model.

4. **Analytics Flags**: Toggle various analytics flags in the sidebar to view different analyses such as:

   * Categorical Column Analysis
   * Receptor Status Distribution
   * Survival Analysis
   * Gene Expression Insights
   * Correlation Heatmap

## Contributing

We welcome contributions to this project! If you have suggestions or improvements, feel free to fork the repository and submit a pull request.

### Contributors

* [Pavan Balaji](https://github.com/pavanbalaji45)
* [Balaji Kartheek](https://github.com/Balaji-Kartheek)

