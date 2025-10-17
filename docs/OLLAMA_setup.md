# Ollama Setup Guide 

## Why should we use Ollama?

✅ **Completely FREE** - No API costs ever  
✅ **Privacy** - Everything runs locally  
✅ **No Rate Limits** - Use as much as we want yay
✅ **Fast** - No network latency  
✅ **Works Offline** - No internet is required  

## Installation

### Step 1: Install Ollama

#### macOS / Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows:
Download from: https://ollama.com/download/windows

### Step 2: Verify Installation
```bash
ollama --version
```

### Step 3: Pull Models

```bash
# Recommended: Fast and good quality (3GB)
ollama pull llama3.2:3b

# Alternative: Fastest option (1GB)
ollama pull llama3.2:1b

# Alternative: Best quality but slower (7GB)
ollama pull mistral:7b

# For embeddings (required for document search)
ollama pull nomic-embed-text
```

### Step 4: Start Ollama Server

```bash
# Ollama runs automatically, but you can check:
ollama serve
```

### Step 5: Test Ollama

```bash
# Test in terminal
ollama run llama3.2:3b "What is free will?"

# Test API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Why is the sky blue?"
}'
```

## Configuration

### Option 1: Use Ollama (Default - FREE)

Edit `backend/.env`:
```bash
LLM_PROVIDER=ollama
OLLAMA_URL=http://localhost:11434
LLM_MODEL=llama3.2:3b
```

### Option 2: Use OpenAI (Paid)

Edit `backend/.env`:
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key
LLM_MODEL=gpt-4-turbo-preview
```

### Option 3: Use Anthropic (Paid)

Edit `backend/.env`:
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key
LLM_MODEL=claude-3-sonnet-20240229
```

## Running the System with Ollama

### Terminal 1: Start Ollama (if not auto-started)
```bash
ollama serve
```

### Terminal 2: Start Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Terminal 3: Start Frontend
```bash
cd frontend
npm run dev
```

## Troubleshooting - common issues & solutions

### Issue: "Connection refused" to Ollama
**Check if Ollama is running:**
```bash
curl http://localhost:11434/api/tags
```

**Start Ollama:**
```bash
ollama serve
```

### Issue: Model not found
**Pull the model:**
```bash
ollama pull llama3.2:3b
```

**List available models:**
```bash
ollama list
```

### Issue: Slow responses
**Try a smaller model:**
```bash
ollama pull llama3.2:1b
```

Update `.env`:
```bash
LLM_MODEL=llama3.2:1b
```

### Issue: Out of memory
**Check RAM usage:**
```bash
ollama ps
```

**Use smaller model or increase system RAM**

## Performance Optimization

### For Faster Responses:
```bash
# Use 1B model
LLM_MODEL=llama3.2:1b
LLM_MAX_TOKENS=500  # Reduce tokens
```

### For Better Quality:
```bash
# Use 7B model
LLM_MODEL=mistral:7b
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
```

### For Balance:
```bash
# Default settings (recommended)
LLM_MODEL=llama3.2:3b
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
```

## Advanced: Custom Models

### Use Llama 3.1 (Larger):
```bash
ollama pull llama3.1:8b
```

### Use Code-Specific Models:
```bash
ollama pull codellama:7b
```

### Use Specialized Models:
```bash
# For medical debates
ollama pull meditron

# For legal debates
ollama pull wizard-vicuna-uncensored
```

## Docker Setup with Ollama

Update `docker-compose.yml`:
```yaml
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - LLM_PROVIDER=ollama
      - OLLAMA_URL=http://ollama:11434
      - LLM_MODEL=llama3.2:3b
    depends_on:
      - ollama

volumes:
  ollama_data:
```


**Ollama is perfect for:**
- Development and testing
- Students and learners
- Privacy-conscious users
- Unlimited experimentation
- Offline usage

## Quick Commands Reference

```bash
# List all models
ollama list

# Pull a model
ollama pull llama3.2:3b

# Remove a model
ollama rm llama3.2:3b

# Run model interactively
ollama run llama3.2:3b

# Check running models
ollama ps

# Stop Ollama
pkill ollama  # Linux/Mac
```

## System Requirements

### Minimum:
- CPU: 4 cores
- RAM: 8 GB
- Disk: 10 GB free
- OS: Windows 10+, macOS 11+, Linux

### Recommended:
- CPU: 8 cores
- RAM: 16 GB
- Disk: 20 GB SSD
- OS: Latest stable
- GPU: Optional (NVIDIA for acceleration)

## GPU Acceleration (Optional)

### With NVIDIA GPU:
Ollama automatically uses GPU if available.

**Check GPU usage:**
```bash
nvidia-smi
```

### Expected Performance:
- CPU only: 10-20 tokens/sec
- With GPU: 50-100 tokens/sec

## Ready to Go!

Your system now runs **100% FREE** with Ollama! 🎉

No API keys needed, unlimited usage, complete privacy.
