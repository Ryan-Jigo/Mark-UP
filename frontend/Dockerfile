# Stage 1: Build the frontend
FROM node:20-alpine AS build

WORKDIR /workspace

# Copy package files from root to install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy the frontend source code
COPY frontend ./frontend

# Build the frontend (outputs to frontend/dist)
RUN npm run build

# Stage 2: Serve the built application with Nginx
FROM nginx:alpine

# Copy built frontend assets
COPY --from=build /workspace/frontend/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
