from setuptools import setup, find_packages

setup(
    name="context-aware-code-search",
    version="1.0.0",
    description="A semantic search engine for source code using Transformer-based embeddings.",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "torch>=2.1.0",
        "transformers>=4.36.0",
        "numpy>=1.24.0",
        "tqdm>=4.66.0",
        "flask>=3.0.0",
        "flask-cors>=4.0.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'code-search=main:run_cli',
        ],
    },
    python_requires='>=3.8',
)
