
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css
COPY script.js /usr/share/nginx/html/script.js

EXPOSE 80

CMD ["sh", "-c", "echo ''; echo '========================================'; echo ' Online Event Registration System'; echo ' Website URL: http://localhost:8083'; echo '========================================'; echo ''; exec nginx -g 'daemon off;'"]
