# MarketingNotes.ai - Docker Image

[![Docker Pulls](https://img.shields.io/docker/pulls/marketingnotes/marketingnotes-oss)](https://hub.docker.com/r/marketingnotes/marketingnotes-oss)
[![Docker Image Size](https://img.shields.io/docker/image-size/marketingnotes/marketingnotes-oss)](https://hub.docker.com/r/marketingnotes/marketingnotes-oss)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful AI-powered communication assistant for entrepreneurs and professionals, now available as a Docker image for easy deployment.

## Quick Start

### Using Docker Compose (Recommended)

1. Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_DB: marketingnotes
      POSTGRES_USER: marketingnotes_user
      POSTGRES_PASSWORD: your-secure-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: pg_isready -d marketingnotes -U marketingnotes_user
      interval: 2s
      timeout: 10s
      retries: 5

  web:
    image: marketingnotes/marketingnotes-oss:latest
    ports:
      - "8000:8000"
    environment:
      DEBUG: "True"
      SECRET_KEY: your-secret-key-here
      POSTGRES_DB: marketingnotes
      POSTGRES_USER: marketingnotes_user
      POSTGRES_PASSWORD: your-secure-password
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

volumes:
  postgres_data:
```

2. Start the application:

```bash
docker-compose up -d
```

3. Open your browser and navigate to `http://localhost:8000`

4. Configure your AI API keys through the web interface (click the key icon 🔑 in the navigation bar)

### Using Docker Run

```bash
# Pull the image
docker pull marketingnotes/marketingnotes-oss:latest

# Run with PostgreSQL
docker run -d \
  --name marketingnotes-db \
  -e POSTGRES_DB=marketingnotes \
  -e POSTGRES_USER=marketingnotes_user \
  -e POSTGRES_PASSWORD=your-secure-password \
  postgres:17

# Run the application
docker run -d \
  --name marketingnotes-app \
  -p 8000:8000 \
  -e DEBUG=True \
  -e SECRET_KEY=your-secret-key-here \
  -e POSTGRES_DB=marketingnotes \
  -e POSTGRES_USER=marketingnotes_user \
  -e POSTGRES_PASSWORD=your-secure-password \
  -e POSTGRES_HOST=host.docker.internal \
  -e POSTGRES_PORT=5432 \
  --link marketingnotes-db:db \
  marketingnotes/marketingnotes-oss:latest
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEBUG` | Django debug mode | `True` | No |
| `SECRET_KEY` | Django secret key | - | Yes |
| `POSTGRES_DB` | Database name | `marketingnotes` | No |
| `POSTGRES_USER` | Database user | `marketingnotes_user` | No |
| `POSTGRES_PASSWORD` | Database password | - | Yes |
| `POSTGRES_HOST` | Database host | `db` | No |
| `POSTGRES_PORT` | Database port | `5432` | No |
| `OPENAI_API_KEY` | OpenAI API key | - | No* |
| `GOOGLE_API_KEY` | Google AI API key | - | No* |

*API keys are configured through the web interface after starting the application

## Features

- **Multi-AI Support**: OpenAI GPT-4, Google Gemini, Anthropic Claude
- **Conversation Management**: Organize and manage multiple chat conversations
- **Custom Response Editor**: Build and customize responses
- **API Key Management**: Secure interface for managing AI service API keys
- **Open Source**: Fully open source with MIT license

## Support

- **GitHub**: [https://github.com/yourusername/marketingnotes_oss](https://github.com/yourusername/marketingnotes_oss)
- **Issues**: [https://github.com/yourusername/marketingnotes_oss/issues](https://github.com/yourusername/marketingnotes_oss/issues)
- **Documentation**: [https://github.com/yourusername/marketingnotes_oss/blob/main/README.md](https://github.com/yourusername/marketingnotes_oss/blob/main/README.md)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/yourusername/marketingnotes_oss/blob/main/LICENSE) file for details. 