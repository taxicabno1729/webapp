# Llama 2 AI Assistant Web Application
A Streamlit-based web application that provides AI-powered analysis and interaction using Llama 2.

## Features
- 🤖 Interactive Chatbot powered by Llama 2
- 🔍 Website Content Analysis
- 📷 Image Text Analysis with OCR
- Real-time AI-powered responses
- Customizable model parameters

## Deployment Options

### Option 1: Docker Deployment (Recommended)
1. Install Docker and Docker Compose on your system
2. Clone the repository:
   ```bash
   git clone https://github.com/taxicabno1729/webapp.git
   cd webapp
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

4. Wait for Ollama to download the Llama 2 model (first run only)
   ```bash
   docker exec -it webapp-ollama-1 ollama pull llama3.2
   ```

5. Access the application at `http://localhost:8501`

### Option 2: Local Installation

#### Prerequisites
- Python 3.x
- pip (Python package installer)
- Ollama with Llama 2 model installed and running locally
- Tesseract OCR installed on your system

#### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/taxicabno1729/webapp.git
   cd webapp
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Ollama and the Llama 2 model:
   - Follow instructions at [Ollama's website](https://ollama.ai) to install Ollama
   - Pull the Llama 3.2 model:
     ```bash
     ollama pull llama3.2
     ```

5. Install Tesseract OCR:
   - **Linux**: `sudo apt-get install tesseract-ocr`
   - **macOS**: `brew install tesseract`
   - **Windows**: Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

#### Running the Application Locally
1. Start the Ollama server:
   ```bash
   ollama serve
   ```

2. In a new terminal, run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to `http://localhost:8501`


### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License
