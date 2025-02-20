# RAG Streamlit Application 🚀

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-green)

A modern Retrieval-Augmented Generation (RAG) application built with Streamlit for document processing and AI-powered question answering.

## Features ✨

- 📄 PDF document processing and text extraction
- 🧠 Integration with state-of-the-art language models
- 🔍 Semantic search capabilities
- 📊 Interactive visualization of results
- ⚙️ Customizable configuration via YAML files
- 📈 Comprehensive logging system

## Installation 🛠️

```bash
# Clone the repository
git clone https://github.com/yourusername/streamlit-rag-application.git

# Install dependencies
pip install -r requirements.txt
```

## Usage 🚀

```bash
streamlit run app.py
```

## Configuration ⚙️

Configure the application through `config.yaml`:
```yaml
model_settings:
  model_name: "gpt-4"
  temperature: 0.7
  max_tokens: 1000

processing:
  chunk_size: 512
  overlap: 50
```

## Project Structure 📁

```
.
├── app.py               # Main Streamlit application
├── config.yaml          # Configuration settings
├── requirements.txt     # Dependency list
├── logs/                # Application logs
├── pdfs/                # PDF documents for processing
└── src/
    ├── config/          # Configuration management
    ├── models/          # RAG model implementations
    ├── processors/      # Document processing modules
    └── utils/           # Utility functions and logging
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
