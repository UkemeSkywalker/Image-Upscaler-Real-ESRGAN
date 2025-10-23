#!/bin/bash

echo "Installing Real-ESRGAN server as a system service..."

# Copy service file to systemd directory
sudo cp realesrgan-server.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable realesrgan-server

# Start the service now
sudo systemctl start realesrgan-server

echo "Service installed and started!"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status realesrgan-server    # Check status"
echo "  sudo systemctl stop realesrgan-server     # Stop service"
echo "  sudo systemctl start realesrgan-server    # Start service"
echo "  sudo systemctl restart realesrgan-server  # Restart service"
echo "  sudo journalctl -u realesrgan-server -f   # View logs"