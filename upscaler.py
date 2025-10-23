import os
import subprocess
import tempfile
import shutil

class ImageUpscaler:
    def __init__(self):
        self.available_models = self._check_available_models()
    
    def _check_available_models(self):
        """Check which models are available"""
        models = {}
        model_files = {
            'general': 'weights/RealESRGAN_x4plus.pth',
            'anime': 'weights/RealESRGAN_x4plus_anime_6B.pth'
        }
        
        for name, path in model_files.items():
            if os.path.exists(path):
                models[name] = {
                    'model_name': 'RealESRGAN_x4plus' if name == 'general' else 'RealESRGAN_x4plus_anime_6B',
                    'path': path
                }
                print(f"Found {name} model")
        
        return models
    
    def upscale_image(self, image_bytes: bytes, model_type: str = 'general', scale: float = 4.0):
        """Upscale image using subprocess call to inference script"""
        if model_type not in self.available_models:
            raise ValueError(f"Model {model_type} not available. Available: {list(self.available_models.keys())}")
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as input_file:
            input_file.write(image_bytes)
            input_path = input_file.name
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Run inference
                model_name = self.available_models[model_type]['model_name']
                cmd = [
                    '/usr/bin/python3', 'inference_realesrgan.py',
                    '-n', model_name,
                    '-i', input_path,
                    '-o', temp_dir,
                    '--outscale', str(scale)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, cwd='.')
                
                if result.returncode != 0:
                    raise RuntimeError(f"Inference failed: {result.stderr}")
                
                # Find output file
                output_files = [f for f in os.listdir(temp_dir) if f.endswith(('.png', '.jpg'))]
                if not output_files:
                    raise RuntimeError("No output file generated")
                
                output_path = os.path.join(temp_dir, output_files[0])
                
                # Read result
                with open(output_path, 'rb') as f:
                    return f.read()
                    
            finally:
                # Clean up input file
                if os.path.exists(input_path):
                    os.unlink(input_path)
    
    def get_available_models(self):
        """Get list of available models"""
        return list(self.available_models.keys())