# Context-Aware Codebase Search Engine (Dev Semantic Search) 🚀

## Overview
This project implements a professional, semantic search engine for source code. Unlike traditional keyword-based search, this system understands the context and meaning of code snippets using state-of-the-art transformer-based embeddings.

The system is designed to help developers find relevant code snippets based on natural language queries like *"how to read a file"* or *"calculate mean of an array"*.

## Key Features 🌟
- **Semantic Understanding**: Uses Transformer-based embeddings (e.g., CodeBERT) to capture code semantics.
- **Top-K Ranking**: Returns results ranked by similarity score.
- **Robust CLI Interface**: Easily perform queries from the terminal.
- **RESTful API**: Includes a Flask-based API for integration with web applications.
- **Professional Logging**: Integrated system for tracking queries and system status.
- **Centralized Config**: Easy model and path management via pp/config/settings.py.

## Project Architecture 🏗️
- \pp/core/\: Core semantic search logic and model handling.
- \pp/cli/\: Terminal interface for the search engine.
- \pp/api/\: REST API server using Flask.
- \pp/utils/\: Common utilities including a centralized logging system.
- \pp/config/\: System-wide configuration settings.
- \data/\: Sample datasets and code snippets.
- \logs/\: Application execution logs.

## Getting Started 🚀

### Prerequisites
- Python 3.8+
- PyTorch
- HuggingFace Transformers

### Installation
1. Clone the repository:
   \\\ash
   git clone https://github.com/yourusername/context-aware-code-search.git
   cd context-aware-code-search
   \\\
2. Install dependencies:
   \\\ash
   pip install -r requirements.txt
   \\\
   *Optional: Install as a local package:*
   \\\ash
   pip install -e .
   \\\

### Usage 🛠️

#### 1. Using the CLI
Run a semantic search query directly from your terminal:
\\\ash
python main.py "find maximum value in array"
\\\
Or use the installed command (if installed via \pip install -e .\):
\\\ash
code-search "find maximum value in array"
\\\

#### 2. Using the REST API
Start the server:
\\\ash
python -m app.api.server
\\\
Make a search request:
\\\ash
curl -X POST http://localhost:5000/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "how to read text from file", "top_k": 3}'
\\\

## Methodology 🧠
The search engine works by mapping both natural language queries and code snippets into a shared high-dimensional vector space. We use a pre-trained Transformer model (e.g., \microsoft/codebert-base\) as the encoder.
1. **Indexing**: Code snippets are encoded into vectors during startup or indexing phase.
2. **Encoding Query**: Natural language queries are encoded into a vector at runtime.
3. **Similarity Search**: Cosine similarity is calculated between the query vector and all code vectors.
4. **Ranking**: Results are sorted and presented based on their similarity scores.

## Future Improvements 📈
- **IDE Plugin**: Integrate with VS Code or IntelliJ.
- **Persistent Indexing**: Support for indexing massive codebases using vector databases like FAISS or ChromaDB.
- **Multi-language Support**: Expand beyond Python to other programming languages.
- **Hybrid Search**: Combine semantic search with BM25 keyword matching for better accuracy.

## Author ✍️
**[Your Name]**
B.Tech 3rd Year, Computer Science and Engineering
University Name
