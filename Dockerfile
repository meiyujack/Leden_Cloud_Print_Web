FROM ghcr.io/astral-sh/uv:alpine
RUN apk add curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
WORKDIR /app
COPY api .
RUN uv sync --frozen
ENV PATH="/root/.local/bin/:$PATH"
CMD ["uv","run","gunicorn","-w","2","-b","0.0.0.0:5000","app:app"]
