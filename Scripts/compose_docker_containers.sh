cd ..
docker-compose up

# Running via docker requires 
# - flask to expose port 0.0.0.0 instead of localhost.
# - cloudflared forwarding traffic to findz-container instead of localhost (Set in Cloudflare Tunnel dashboard)