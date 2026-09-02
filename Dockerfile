# Stage 1: Build React Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend & Static Serving
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code and built frontend
COPY backend/ ./backend/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Build SQLite database with all 182+ player profiles
WORKDIR /app/backend
RUN python pipeline/build_db.py

# Expose port (Default 8000, Render sets $PORT dynamically)
EXPOSE 8000
ENV PORT=8000

# Start production server
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
