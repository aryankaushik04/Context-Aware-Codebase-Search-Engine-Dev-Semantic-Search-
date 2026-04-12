# Context-Aware Codebase Search Engine

## Overview
A semantic search engine for code that understands the intent behind natural language queries instead of relying only on keywords.


## Why I Built This
As a 3rd year CSE student, I often faced difficulty while searching for relevant code across multiple files and projects.
Traditional keyword search was not effective because it does not understand the actual meaning of the query.
This project is my attempt to solve that problem using transformer-based embeddings.

## What It Does
* Takes a natural language query (e.g., "read a file in python").
* Converts both query and code snippets into vector embeddings.
* Finds similar code using cosine similarity.
* Returns top matching results.


## Tech Stack
* Python
* PyTorch
* HuggingFace Transformers (CodeBERT)
* Flask (for API)


## How It Works
1. Code snippets are converted into embeddings using CodeBERT.
2. User query is also encoded into a vector.
3. Cosine similarity is computed.
4. Top-K similar code snippets are returned.


## My Contributions / Improvements
* Refactored folder structure for better understanding
* Improved CLI interface for easier usage
* Added logging for debugging
* Cleaned configuration handling
* Made the project more modular


## Challenges I Faced
* Understanding how embeddings represent code semantics.
* Handling similarity search efficiently.
* Structuring the project in a clean and modular way.


## Future Improvements
* Use FAISS / vector DB for faster search.
* Add support for multiple languages.
* Build a simple web interface.


## Inspiration
This project was inspired by existing implementations of semantic code search systems. 
I explored different approaches and built my own version with modifications and improvements.

## Author
**Aryan Kaushik**


Computer Science and Engineering


RGIPT Amethi
