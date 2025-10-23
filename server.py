from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from upscaler import ImageUpscaler
import logging
from logging.handlers import RotatingFileHandler
import asyncio
import os

# Setup logging to file with rotation
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            os.path.join(log_dir, "realesrgan-server.log"),
            maxBytes=10*1024*1024,  # 10MB per file
            backupCount=5  # Keep 5 backup files
        ),
        logging.StreamHandler()  # Also log to console
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Real-ESRGAN Image Upscaler", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://pq8iuiyjvg.us-east-1.awsapprunner.com", "https://d2qxv8n4kginy3.cloudfront.net"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Initialize upscaler
upscaler = ImageUpscaler()

# Concurrency control - limit to 3 concurrent GPU processes
processing_semaphore = asyncio.Semaphore(3)

@app.get("/")
async def root():
    return {"message": "Real-ESRGAN Image Upscaler Server", "models": upscaler.get_available_models()}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "available_models": upscaler.get_available_models(),
        "concurrent_limit": 3,
        "available_slots": processing_semaphore._value
    }

@app.post("/upscale")
async def upscale_image(
    file: UploadFile = File(...),
    model: str = Query(default="general", description="Model type: general or anime"),
    scale: float = Query(default=4.0, ge=1.0, le=8.0, description="Upscale factor (1.0-8.0)")
):
    """Upscale an image using Real-ESRGAN"""
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Acquire semaphore to limit concurrent processing
    async with processing_semaphore:
        try:
            # Read image bytes
            image_bytes = await file.read()
            logger.info(f"Processing image: {file.filename}, model: {model}, scale: {scale} (Queue position acquired)")
            
            # Upscale image (run in thread pool to avoid blocking)
            loop = asyncio.get_event_loop()
            result_bytes = await loop.run_in_executor(
                None, 
                upscaler.upscale_image, 
                image_bytes, 
                model, 
                scale
            )
            
            logger.info(f"Completed processing: {file.filename}")
            
            # Return upscaled image
            return Response(
                content=result_bytes,
                media_type="image/png",
                headers={"Content-Disposition": f"attachment; filename=upscaled_{file.filename}"}
            )
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)