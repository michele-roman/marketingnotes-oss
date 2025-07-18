# MarketingNotes.ai - Open Source

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://www.djangoproject.com/)

A powerful AI-powered communication assistant for entrepreneurs and professionals to build meaningful customer relationships through personalized emails, messages, strategies, and content.

**🚀 Ready to run with Docker Desktop in minutes!**

## Features

- **Multi-AI Support**: Integrates with OpenAI GPT-4, Google Gemini, and Anthropic Claude
- **Custom Response Editor**: Build and customize responses using an interactive editor
- **API Key Management**: Secure, user-friendly interface for managing AI service API keys
- **Open Source**: Fully open source, allowing users to run their own instance with their own API keys

## Quick Start

### Option 1: Docker (Recommended)

The easiest way to run MarketingNotes.ai-OSS is using Docker Desktop. Each user gets their own isolated environment with local data persistence.

#### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- API keys for your preferred AI services

#### Installation with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd marketingnotes_oss
```

2. Set up your local environment:
```bash
cp env.example .env.docker
```

3. Edit `.env.docker` with your own settings:
   - Generate a secure `SECRET_KEY` (run: `python scripts/generate-secret.py`)
   - Set a strong `POSTGRES_PASSWORD`
   
   **Note:** AI API keys are added through the web interface after starting the application

4. Start the application:
```bash
docker-compose up -d
```

5. Open your browser and navigate to `http://localhost:8000`

6. To stop the application:
```bash
docker-compose down
```

### Option 2: Local Development

#### Prerequisites

- Python 3.8+
- Poetry (for dependency management)
- PostgreSQL database
- API keys for your preferred AI services

#### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd marketingnotes_oss
```

2. Install dependencies:
```bash
poetry install
```

3. Set up your environment variables (copy from `env.example`)

4. Run migrations:
```bash
poetry run python manage.py migrate
```

5. Create a superuser (optional):
```bash
poetry run python manage.py createsuperuser
```

6. Start the development server:
```bash
poetry run python manage.py runserver
```

7. Open your browser and navigate to `http://localhost:8000`

## API Keys Configuration

After starting the application, you need to configure your API keys through the web interface:

1. Open your browser and navigate to `http://localhost:8000`
2. Click the key icon (🔑) in the top navigation bar
3. Enter your API keys for the services you want to use:
   - **OpenAI**: Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - **Google Gemini**: Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **Anthropic Claude**: Get your key from [Anthropic Console](https://console.anthropic.com/)

### Security

- API keys are stored securely in your local database
- Keys are never shared with third parties or stored in environment files
- Each user manages their own API keys through the web interface
- Keys are only used to communicate with the respective AI services

## Usage

### Starting a Conversation

1. Navigate to the chat interface
2. Type your message in the input field
3. The system will generate responses from all configured AI services
4. Choose the best response or use the custom editor to create your own

### Managing Conversations

- Create new chats for different topics or clients
- View conversation history
- Edit chat names for better organization
- Switch between different conversations

### Custom Response Editor

- Use the custom response option to build personalized responses
- Combine elements from different AI responses

## Docker

### Why Docker?

- **Easy Setup**: No need to install Python, PostgreSQL, or other dependencies
- **Consistent Environment**: Works the same way on any operating system
- **Isolated**: Doesn't interfere with your existing development environment
- **Production Ready**: The same setup can be used in production
- **Local Configuration**: Each user manages their own environment variables locally
- **Secure**: Sensitive data (API keys, passwords) stays on your local machine

### Docker Compose Services

The application runs with two services:

- **Web**: Django application server
- **DB**: PostgreSQL database

### Local Data Persistence

Your data is stored in local Docker volumes:

- **Database**: `postgres_data` volume stores all your conversations and settings
- **Environment**: `.env.docker` file contains your personal configuration
- **Code**: The application code is mounted from your local directory for development

This means:
- Your data persists between container restarts
- Each user has their own isolated environment
- You can easily backup your data by copying the Docker volumes

### Environment Variables

Each user creates their own `.env.docker` file locally:

```bash
# Copy the template
cp env.example .env.docker

# Edit with your own values
nano .env.docker  # or use your preferred editor
```

**Required settings:**
```bash
SECRET_KEY=your-secret-key-here  # Generate with: python -c "import secrets; print(secrets.token_urlsafe(50))"
POSTGRES_PASSWORD=your-secure-password
```

**Important:** The `.env.docker` file is in `.gitignore` and will never be committed to the repository. Each user manages their own environment locally.

**API Keys:** AI service API keys are added through the web interface after starting the application, not in the environment file.

### Docker Commands

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down

# Rebuild after changes
docker-compose up -d --build

# Access the database
docker-compose exec db psql -U marketingnotes_user -d marketingnotes
```

## Development

```
marketingnotes_oss/
├── app/                    # Main Django application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # URL routing
│   ├── agent.py           # AI agent implementations
│   └── admin.py           # Django admin configuration
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── api_keys.html      # API keys management page
│   └── chat/              # Chat-related templates
├── static/                # Static files (CSS, JS, images)
└── marketingnotes_oss/    # Django project settings
```

### Adding New AI Services

To add support for a new AI service:

1. Add the service to the `SERVICE_CHOICES` in `app/models.py`
2. Create a new agent function in `app/agent.py`
3. Update the `send_message` view in `app/views.py`
4. Add the corresponding message model if needed

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

## Roadmap

- [ ] Function validation for Marketingnotes.ai further development
- [ ] Integration with Marketingnotes.ai
- [ ] Contribute to developer community
- [ ] Research of interested people
- [ ] Research for startup co-founder
- [ ] Open innovation through software sharing
