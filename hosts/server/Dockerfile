# Use official python slim image for smaller footprint
FROM python:3.15-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpcap-dev build-essential

RUN sysctl -w net.ipv4.tcp_window_scaling=0 \
            net.ipv4.tcp_syncookies=0 \
            net.ipv4.tcp_mss=1460

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (adjust paths based on your structure)
COPY ./src/ .

EXPOSE 5000
EXPOSE 12345
CMD ["python", "app.py"]
