# Semantic Code Search

This module implements a semantic search system for code using CodeBERT.

## Introduction
The goal is to find the most relevant code snippet given a natural language query.

## Usage

### Data Preprocessing
Prepare your dataset in JSONL format with NL-PL pairs.

### Training
```bash
python run_classifier.py --do_train --do_eval --model_type roberta --model_name_or_path microsoft/codebert-base --train_filename $train_file --dev_filename $dev_file --output_dir $output_dir
```

### Evaluation
```bash
python run_classifier.py --do_test --model_type roberta --model_name_or_path microsoft/codebert-base --load_model_path $test_model --test_filename $test_file
```

## Results
We evaluate the model using Mean Reciprocal Rank (MRR).
