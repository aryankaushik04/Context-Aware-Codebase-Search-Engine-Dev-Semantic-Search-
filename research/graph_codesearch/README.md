# Semantic Code Search with GraphCodeBERT

This module uses GraphCodeBERT, which incorporates code data flow information for improved code search.

## Overview
By building data flow graphs (DFG), GraphCodeBERT better captures the structural and semantic dependencies within the code.

## Getting Started

### Data Flow Graph Generation
The code for generating DFGs from source code is provided in the `parser/` folder.

### Usage
Training the model with data flow information:
```bash
python run.py --do_train --do_eval --model_type roberta --model_name_or_path microsoft/graphcodebert-base --train_filename $train_file --dev_filename $dev_file --output_dir $output_dir
```

## Advantages
- Better understanding of variable dependencies.
- Improved performance on complex code structures.
