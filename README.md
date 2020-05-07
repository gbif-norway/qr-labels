# Run with
docker build --tag qr:latest .
docker run -d --network=nginx-proxy --name qr qr:latest
