# Real-ESRGAN Image Upscaler Server

A FastAPI-based web server for image upscaling using Real-ESRGAN.

## Quick Start

1. **Setup:**
   ```bash
   ./setup_server.sh
   ```

2. **Start server:**
   ```bash
   python server.py
   ```

3. **Access:**
   - Server: http://localhost:8000
   - API docs: http://localhost:8000/docs

## API Endpoints

### POST /upscale
Upload and upscale an image.

**Parameters:**
- `file`: Image file (required)
- `model`: Model type - "general" or "anime" (default: "general")
- `scale`: Upscale factor 1.0-8.0 (default: 4.0)

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/upscale?model=general&scale=4.0" \
     -H "accept: image/png" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_image.jpg" \
     --output upscaled_image.png
```

### GET /health
Check server status and available models.

### GET /
Server info and available models.

## Models

- **general**: Best for photos and realistic images
- **anime**: Optimized for anime/cartoon images

Models are automatically downloaded during setup.