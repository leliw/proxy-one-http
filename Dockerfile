# ------ Stage 1: Angular project ------
    FROM node:20 AS angular-build
    WORKDIR /app

    COPY frontend/package.json frontend/package-lock.json ./
    RUN npm install
    
    COPY frontend/ .
    RUN npm run build
    
# ------ Stage 2: Python/FastAPI project ------
    FROM python:3.12.4-slim
    WORKDIR /app
    
    # Keeps Python from generating .pyc files in the container
    ENV PYTHONDONTWRITEBYTECODE=1
    # Turns off buffering for easier container logging
    ENV PYTHONUNBUFFERED=1
    RUN python -m pip install --upgrade pip
    # Install pip requirements
    COPY backend/requirements.txt .
    RUN python -m pip install -r requirements.txt
    
    COPY ./backend/ /app
    # Copy Angular build to FastAPI static folder
    COPY --from=angular-build /app/dist/frontend /app/static
    
    # Creates a non-root user with an explicit UID and adds permission to access the /app folder
    # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
    RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
    RUN mkdir /storage && mkdir /workspace
    RUN chown -R appuser /storage && chown -R appuser /workspace
    
    USER appuser
    VOLUME /storage
    VOLUME /workspace
    EXPOSE 8080
    CMD ["gunicorn", "--bind", "0.0.0.0:8080", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]