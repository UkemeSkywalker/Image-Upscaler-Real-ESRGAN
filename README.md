# Real-ESRGAN Image Upscaler Server

A production-ready FastAPI server for image upscaling using Real-ESRGAN with concurrent processing support.

## Features

- **Multiple Models**: General photos and anime-optimized models
- **Concurrent Processing**: Handles 2-10 users with queue management
- **Auto-restart**: Systemd service with automatic startup
- **CORS Support**: Cross-origin requests from frontend applications
- **Health Monitoring**: Status endpoints and logging

## Quick Start

### 1. Setup
```bash
# Run the automated setup
./setup_server.sh
```

### 2. Install as System Service
```bash
# Install and start the service
./install_service.sh
```

### 3. Test the Server
```bash
# Check health
curl http://localhost:8000/health

# Test upscaling
curl -X POST "http://localhost:8000/upscale?model=general&scale=4.0" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@inputs/0014.png" \
     --output result.png
```

## API Endpoints

### POST /upscale
Upload and upscale an image.

**Parameters:**
- `file`: Image file (required)
- `model`: "general" or "anime" (default: "general")
- `scale`: Upscale factor 1.0-8.0 (default: 4.0)

**Example:**
```bash
curl -X POST "http://your-server:8000/upscale?model=anime&scale=2.0" \
     -F "file=@image.jpg" \
     --output upscaled.png
```

### GET /health
Check server status and queue information.

**Response:**
```json
{
  "status": "healthy",
  "available_models": ["general", "anime"],
  "concurrent_limit": 3,
  "available_slots": 2
}
```

### GET /
Server information and available models.

## Service Management

```bash
# Check status
sudo systemctl status realesrgan-server

# Start/stop/restart
sudo systemctl start realesrgan-server
sudo systemctl stop realesrgan-server
sudo systemctl restart realesrgan-server

# View logs
sudo journalctl -u realesrgan-server -f
```

## Configuration

### CORS Settings
Currently allows requests from any IP on port 3000. Edit `server.py` to modify:

```python
allow_origin_regex=r"http://.*:3000"  # Any IP on port 3000
# OR
allow_origins=["http://your-frontend-domain.com"]  # Specific domain
```

### Concurrency Limit
Adjust concurrent processing limit in `server.py`:

```python
processing_semaphore = asyncio.Semaphore(3)  # Max 3 concurrent jobs
```

## Models

- **General** (`RealESRGAN_x4plus`): Best for photos and realistic images
- **Anime** (`RealESRGAN_x4plus_anime_6B`): Optimized for anime/cartoon images

Models are automatically downloaded during setup (~300MB total).

## Troubleshooting

### Check Logs
```bash
sudo journalctl -u realesrgan-server -f
```

### Common Issues

**Port already in use:**
```bash
sudo pkill -f "python3 server.py"
sudo systemctl restart realesrgan-server
```

**GPU memory issues:**
- Reduce concurrent limit in `server.py`
- Use smaller scale factors
- Process smaller images

**Service won't start:**
```bash
sudo systemctl status realesrgan-server
sudo journalctl -u realesrgan-server --no-pager -n 20
```

## File Structure

```
Image-Upscaler-Real-ESRGAN/
├── server.py                 # Main FastAPI server
├── upscaler.py              # Real-ESRGAN wrapper
├── inference_realesrgan.py  # Core inference script
├── setup_server.sh          # Automated setup
├── install_service.sh       # Service installation
├── realesrgan-server.service # Systemd service file
├── requirements*.txt        # Dependencies
├── weights/                 # Model files
└── inputs/                  # Test images
```

## Requirements

- Python 3.7+
- CUDA-compatible GPU (recommended)
- Ubuntu/Linux system with systemd
- ~2GB disk space for models

## Performance

- **Concurrent Users**: 2-10 users supported
- **Processing Time**: 5-30 seconds per image (depends on size/GPU)
- **Memory Usage**: ~1-3GB GPU memory per concurrent job
- **Queue Management**: Automatic request queuing when busy

## Security

- CORS configured for specific origins
- Input validation for file types
- Error handling and logging
- Service runs as non-root user