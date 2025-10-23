#!/bin/bash

# Clean up log files older than 7 days
LOG_DIR="/home/ubuntu/Image-Upscaler-Real-ESRGAN/logs"

# Remove log files older than 7 days
find "$LOG_DIR" -name "*.log*" -type f -mtime +7 -delete

# Log the cleanup action
echo "$(date): Cleaned up log files older than 7 days" >> "$LOG_DIR/cleanup.log"