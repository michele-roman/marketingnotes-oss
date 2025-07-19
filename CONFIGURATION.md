# Configuration Guide

## Environment Variables

The application uses sensible defaults, but you can customize the following environment variables:

### Django Settings

```bash
# Debug mode (set to False in production)
DEBUG=True

# Secret key for Django (generate a secure one for production)
SECRET_KEY=your-secret-key-here

# Allowed hosts (comma-separated list)
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# CSRF trusted origins (for HTTPS)
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

### Database Configuration

```bash
# PostgreSQL connection string (optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/marketingnotes

# Example PostgreSQL URLs:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/marketingnotes
# DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### AI Service API Keys

API keys are configured through the web interface after starting the application:

1. Start the application
2. Navigate to `http://localhost:8000`
3. Click the key icon (🔑) in the navigation
4. Enter your API keys for the services you want to use

**Supported AI Services:**
- **OpenAI**: Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Google Gemini**: Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Anthropic Claude**: Get your key from [Anthropic Console](https://console.anthropic.com/)

## Production Deployment

### Using Environment File

1. Create a `.env` file:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your production settings:
```bash
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=postgresql://user:password@host:5432/marketingnotes
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

3. Start with environment file:
```bash
docker-compose --env-file .env up -d
```

### Using Docker Environment Variables

```bash
docker run -d \
  -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e ALLOWED_HOSTS=yourdomain.com \
  marketingnotes-oss:latest
```

## Security Best Practices

1. **Generate a secure SECRET_KEY**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

2. **Use HTTPS in production**:
   - Set up SSL/TLS certificates
   - Configure `CSRF_TRUSTED_ORIGINS`
   - Use secure database connections

3. **Database security**:
   - Use strong passwords
   - Restrict database access
   - Regular backups

4. **API Key security**:
   - Rotate API keys regularly
   - Monitor API usage
   - Use environment variables for sensitive data

## Troubleshooting

### Common Issues

1. **Database connection errors**:
   - Check `DATABASE_URL` format
   - Ensure database is running
   - Verify credentials

2. **Static files not loading**:
   - Run `python manage.py collectstatic`
   - Check WhiteNoise configuration
   - Verify file permissions

3. **Tailwind CSS not working**:
   - Run `npm run build:css`
   - Check `tailwind.config.js`
   - Verify template paths

### Logs and Debugging

```bash
# View application logs
docker-compose logs -f web

# View database logs
docker-compose logs -f db

# Access Django shell
docker-compose exec web poetry run python manage.py shell

# Check database
docker-compose exec db psql -U postgres -d marketingnotes
``` 