# UniXcoder: Unified Code Representation

This module implements UniXcoder, a unified model for various code understanding and generation tasks.

## Key Features
- **Unified Architecture**: Supports both understanding and generation.
- **Cross-Modal**: Trained on both natural language and programming language.

## Usage

### Using UniXcoder for Embeddings
```python
from unixcoder import UniXcoder
import torch

model = UniXcoder("microsoft/unixcoder-base")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

tokens_ids = model.tokenize(["def add(a, b): return a + b"], max_length=512, mode="<encoder-only>")
source_ids = torch.tensor(tokens_ids).to(device)
_, code_embeddings = model(source_ids)
```

## Applications
- Code Search
- Code Summarization
- Code Generation
- Clone Detection
