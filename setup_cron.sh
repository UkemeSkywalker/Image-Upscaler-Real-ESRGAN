#!/bin/bash

echo "Setting up log cleanup cron job..."

# Add cron job to run cleanup script every 5 days at 2 AM
(crontab -l 2>/dev/null; echo "0 2 */5 * * /home/ubuntu/Image-Upscaler-Real-ESRGAN/cleanup_logs.sh") | crontab -

echo "Cron job added successfully!"
echo "Log cleanup will run every 5 days at 2:00 AM"
echo ""
echo "To verify cron job:"
echo "  crontab -l"
echo ""
echo "To remove cron job:"
echo "  crontab -e  # then delete the cleanup_logs.sh line"