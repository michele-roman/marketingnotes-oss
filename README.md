# MarketingNotes.ai - Open Source Software Release

<div align="center">
  <img src="static/osssvg1.svg" alt="MarketingNotes.ai Logo" width="300" height="auto">
</div>

A powerful AI-powered communication assistant for entrepreneurs and professionals to build meaningful customer relationships through personalized emails, messages, strategies, and content.

**🚀 Ready to run with Docker in minutes!**

## 🎯 The Problem to Solve

When creating content, we often start with a vague idea of what we want but struggle to define the perfect final result. Traditional content creation is limited by our initial vision - we can only create what we can imagine upfront.

However, AI has revealed an interesting phenomenon: **we're excellent at recognizing exceptional results when we see them, even if we couldn't have conceived them initially**. The challenge is that we don't know what our "best possible result" looks like until we encounter it.

**The Solution:**
- **Multiple AI Perspectives**: Generate diverse responses from different LLMs (OpenAI, Gemini, Claude) to explore various creative directions
- **Intelligent Combination**: Merge and edit responses from multiple AI models to create superior results
- **Iterative Refinement**: Continuously improve content by leveraging the strengths of different AI models

This approach dramatically increases the probability of discovering that "perfect result" that exceeds our original expectations - here is the prototype.

## ✨ Features

- **🤖 Multi-AI Support**: Integrates with OpenAI GPT-4, Google Gemini, and Anthropic Claude
- **💬 Custom Response Editor**: Build and customize responses using an interactive editor
- **🐳 Docker-Ready**: Easy deployment with Docker and Docker Compose
- **🔐 Secure API Management**: User-friendly interface for managing AI service API keys

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- API keys for your preferred AI services (optional for initial setup)

### Option 1: Docker Compose (Recommended)

The easiest way to get started:

```bash
# Clone the repository
git clone https://github.com/michele-roman/marketingnotes-oss.git
cd marketingnotes-oss

# Start the application
docker-compose up -d

# Open your browser
open http://localhost:8000
```

### Option 2: Simple Docker Run

For quick testing with SQLite:

```bash
# Clone the repository
git clone https://github.com/michele-roman/marketingnotes-oss.git
cd marketingnotes-oss

# Build and run
docker build -t marketingnotes-oss .
docker run -p 8000:8000 marketingnotes-oss

# Open your browser
open http://localhost:8000
```

### Option 3: Local Development

For developers who want to contribute:

```bash
# Clone the repository
git clone https://github.com/michele-roman/marketingnotes-oss.git
cd marketingnotes-oss

# Install Python dependencies
poetry install

# Install Node.js dependencies
npm install

# Build Tailwind CSS
npm run build:css

# Run migrations
poetry run python manage.py migrate

# Start development server
poetry run python manage.py runserver
```

## 🔧 Configuration

### Environment Variables

The application uses sensible defaults, but you can customize:

```bash
# Database (optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/marketingnotes

# Django settings
DEBUG=True  # Set to False in production
SECRET_KEY=your-secret-key-here
```

### API Keys Setup

After starting the application:

1. Open your browser and navigate to `http://localhost:8000`
2. Click the key icon (🔑) in the top navigation bar
3. Enter your API keys for the services you want to use:
   - **OpenAI**: Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - **Google Gemini**: Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **Anthropic Claude**: Get your key from [Anthropic Console](https://console.anthropic.com/)

## 🐳 Docker Configuration

### Docker Compose Services

The application runs with two services:

- **Web**: Django application server with Tailwind CSS
- **DB**: PostgreSQL database (optional)

### Production Deployment

For production deployment:

```bash
# Create production environment file
cp .env.example .env.prod

# Edit with your production settings
nano .env.prod

# Start with production settings
docker-compose -f docker-compose.prod.yml up -d
```

## 🏗️ Architecture

```
marketingnotes_oss/
├── app/                    # Main Django application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # URL routing
│   ├── agent.py           # AI agent implementations
│   └── admin.py           # Django admin configuration
├── templates/             # HTML templates
│   ├── base.html          # Base template with Tailwind CSS
│   ├── api_keys.html      # API keys management page
│   └── chat/              # Chat-related templates
├── static/                # Static files (CSS, JS, images)
│   ├── input.css          # Tailwind CSS input
│   └── output.css         # Compiled Tailwind CSS
├── marketingnotes_oss/    # Django project settings
└── docker-compose.yml     # Docker configuration
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/michele-roman/marketingnotes-oss.git
   cd marketingnotes-oss
   ```

3. **Set up development environment**:
   ```bash
   poetry install
   npm install
   npm run build:css
   poetry run python manage.py migrate
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

5. **Make your changes and test**:
   ```bash
   poetry run python manage.py runserver
   ```

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add amazing feature"
   git push origin feature/amazing-feature
   ```

7. **Roadmap**:

- [ ] Function validation for Marketingnotes.ai further development
- [ ] Integration with Marketingnotes.ai
- [ ] Contribute to developer community
- [ ] Research of interested people
- [ ] Research for startup co-founder
- [ ] Open innovation through software sharing



## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-green.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4+-38B2AC.svg)](https://tailwindcss.com/)

**Made with ❤️ by the open source community**

</div>
