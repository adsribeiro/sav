FROM python:3.12-slim-bookworm

# Install uv
RUN pip install --upgrade pip

# Copy project files
COPY . /src
WORKDIR /src

# Install production dependencies.
RUN pip install -r requirements.txt


# Expose port
EXPOSE 8501

# Entrypoint
ENTRYPOINT ["streamlit", "run", "login.py", "--server.port=8501"]
