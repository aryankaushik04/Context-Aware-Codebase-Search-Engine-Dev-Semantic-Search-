# Code Documentation Generation

This module focuses on automatically generating natural language documentation for source code across various programming languages.

## Getting Started

### Prerequisites
- Python 3.8+
- PyTorch
- Transformers

### Dataset
We use the CodeSearchNet dataset. You can download and preprocess it using the provided scripts.

## Usage

### Training
To train the model on a specific language:
```bash
python run.py --do_train --do_eval --model_type roberta --model_name_or_path microsoft/codebert-base --train_filename $train_file --dev_filename $dev_file --output_dir $output_dir
```

### Inference
To generate documentation for test code:
```bash
python run.py --do_test --model_type roberta --model_name_or_path microsoft/codebert-base --load_model_path $test_model --test_filename $test_file
```

## Features
- Support for 6 languages: Python, Java, JS, PHP, Ruby, Go.
- Uses CodeBERT as the base transformer model.
- Evaluation using BLEU scores.
