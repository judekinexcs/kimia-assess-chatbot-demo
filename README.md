# 🧬 KIMIA Assess Chatbot

A Streamlit-based chatbot application for querying KIMIA Assess medical imaging data using Qdrant vector database and OpenAI.

## 🚀 Features

- **RAG (Retrieval-Augmented Generation)** with Qdrant vector database
- **Conversational AI** using OpenAI GPT-4
- **Medical Imaging Knowledge Base** for KIMIA Assess platform
- **Real-time Chat Interface** with Streamlit

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: OpenAI GPT-4, LangChain
- **Vector Database**: Qdrant
- **Embeddings**: OpenAI Embeddings

## 📋 Prerequisites

- Python 3.8+
- OpenAI API Key
- Qdrant Cloud account
- Streamlit account

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd KimiaAssessChatBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key"
   QDRANT_URL = "your-qdrant-url"
   QDRANT_API_KEY = "your-qdrant-api-key"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and main file (`app.py`)
   - Add your secrets in the Streamlit Cloud dashboard
   - Deploy!

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ |
| `QDRANT_URL` | Qdrant Cloud URL | ✅ |
| `QDRANT_API_KEY` | Qdrant API key | ✅ |

### Qdrant Collection

Make sure your Qdrant collection is named `kimia_assess` and configured with the correct vector dimensions.

## 📁 Project Structure

```
KimiaAssessChatBot/
├── app.py                 # Main Streamlit application
├── app_fixed.py          # Version with error handling
├── requirements.txt      # Python dependencies
├── .streamlit/
│   └── secrets.toml     # Local secrets (not in git)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the logs in Streamlit Cloud
2. Verify your API keys are correct
3. Ensure Qdrant collection exists and is properly configured
4. Check the [Streamlit documentation](https://docs.streamlit.io) 