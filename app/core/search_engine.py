import os
import json
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from typing import List, Dict, Any, Optional
from app.utils.logger import get_logger
from app.config.settings import Config

logger = get_logger(__name__)

class SemanticCodeSearch:
    """Core class for performing semantic search on code snippets using Transformer-based embeddings."""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initializes the search engine with a specific pre-trained model.
        
        Args:
            model_name: Name of the HuggingFace model card. Defaults to Config.DEFAULT_MODEL_NAME.
        """
        self.model_name = model_name or Config.DEFAULT_MODEL_NAME
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.snippets = []  # List of dicts with 'code', 'description', and 'combined_text'
        
        logger.info(f"Initializing search engine using model: {self.model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info("Model and tokenizer loaded successfully.")
            
            # Ensure data directory exists
            Config.setup_dirs()
            
            # Dynamically load snippets from JSON file
            self._load_snippets()
        except Exception as e:
            logger.error(f"Failed to load search engine: {str(e)}")
            raise

    def _load_snippets(self):
        """Loads all code snippets from data/snippets.json and prepares combined text for better semantic search."""
        snippets_path = os.path.join(Config.DATA_DIR, "snippets.json")
        
        logger.info(f"Loading snippets from: {snippets_path}")
        
        try:
            if not os.path.exists(snippets_path):
                logger.error(f"Error: Snippets file not found at {snippets_path}")
                raise FileNotFoundError(f"Snippets file not found at {snippets_path}")

            with open(snippets_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data:
                logger.error(f"Error: Snippets file {snippets_path} is empty")
                raise ValueError(f"Snippets file {snippets_path} is empty")
            
            # Prepare internal storage with combined description and code
            self.snippets = []
            for item in data:
                if "code" in item and "description" in item:
                    self.snippets.append({
                        "code": item["code"],
                        "description": item["description"],
                        "combined_text": f"{item['description']} {item['code']}"
                    })
            
            if not self.snippets:
                logger.error("Error: No valid snippets with 'code' and 'description' found")
                raise ValueError("No valid snippets with 'code' and 'description' found")

            logger.info(f"Total snippets loaded: {len(self.snippets)}")
            
        except json.JSONDecodeError:
            logger.error(f"Error: Invalid JSON format in {snippets_path}")
        except Exception as e:
            logger.error(f"Error loading snippets: {str(e)}")

    def get_text_embedding(self, text: str) -> torch.Tensor:
        """
        Generates a high-dimensional vector representation of the input text.
        
        Args:
            text: The input natural language query or code snippet.
            
        Returns:
            A torch.Tensor containing the embedding.
        """
        try:
            # CodeBERT recommends using [CLS] token for sequence representation
            # For better results, we follow the standard CodeBERT fine-tuning/inference pattern
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=Config.MAX_SEQUENCE_LENGTH
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # CodeBERT uses RoBERTa architecture where the first token is <s> (mapping to [CLS])
            # We take the hidden state of this first token
            cls_embedding = outputs.last_hidden_state[:, 0, :]
            
            # Normalize embedding for cosine similarity to work as a dot product if needed,
            # though F.cosine_similarity does this internally.
            return F.normalize(cls_embedding, p=2, dim=1)
        except Exception as e:
            logger.error(f"Error generating embedding for text: {text[:50]}... Error: {str(e)}")
            raise

    def search(self, query: str, code_snippets: Optional[List[str]] = None, top_k: int = Config.DEFAULT_TOP_K) -> List[Dict[str, Any]]:
        """
        Performs semantic search to find the most relevant code snippets for a given query.
        
        Args:
            query: The natural language search query.
            code_snippets: Optional list of raw snippets. If provided, these will be used instead of the pre-loaded ones.
            top_k: The number of results to return.
            
        Returns:
            A list of dictionaries containing the code and its similarity score, sorted by relevance.
        """
        logger.info(f"Processing search query: '{query}'")
        
        # 1. Generate query embedding
        query_vec = self.get_text_embedding(query)
        
        # 2. Determine indexing source and generate embeddings
        if code_snippets is not None:
            logger.info(f"Indexing {len(code_snippets)} provided code snippets (raw mode)...")
            texts_to_embed = code_snippets
            return_codes = code_snippets
        else:
            if not self.snippets:
                logger.warning("No code snippets available for search.")
                return []
            
            # Using both description and code often provides better semantic alignment
            # but description carries more weight for NL queries.
            logger.info(f"Indexing {len(self.snippets)} code snippets (enhanced mode)...")
            texts_to_embed = [f"{s['description']} {s['code']}" for s in self.snippets]
            return_codes = [s["code"] for s in self.snippets]
        
        code_vecs = []
        for text in texts_to_embed:
            # CodeBERT works best with a specific format for NL-Code pairs
            # but since we are using it for zero-shot retrieval, we'll keep it simple
            code_vecs.append(self.get_text_embedding(text))
        
        code_matrix = torch.cat(code_vecs, dim=0)
        
        # 3. Calculate cosine similarity
        similarities = F.cosine_similarity(query_vec, code_matrix)
        
        # 4. Rank and format results
        results = []
        for i, score in enumerate(similarities):
            # i is the index in return_codes / texts_to_embed
            # If we used internal snippets, i also maps to self.snippets
            res = {
                "code": return_codes[i],
                "score": float(score.item())
            }
            if code_snippets is None:
                res["description"] = self.snippets[i]["description"]
            results.append(res)
        
        # Sort by similarity score descending
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        
        # Return top-k
        return sorted_results[:top_k]
