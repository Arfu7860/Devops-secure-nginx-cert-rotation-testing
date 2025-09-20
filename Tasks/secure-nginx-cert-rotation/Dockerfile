# Use a standard NGINX image as the base
FROM nginx:1.25.3-alpine

# Copy the initial configuration and certificates
COPY configs/nginx.conf /etc/nginx/conf.d/default.conf
COPY data/certs/initial/ /etc/nginx/certs/

# Expose port 443
EXPOSE 443

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
