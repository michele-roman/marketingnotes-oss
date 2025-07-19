FROM python:3.13-bullseye
ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs

# Install poetry
RUN pip install poetry

# Copy package files
COPY pyproject.toml poetry.lock ./
COPY package.json package-lock.json* ./

# Install Python dependencies
RUN poetry install --no-root

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build Tailwind CSS with updated config
RUN npx tailwindcss -i ./static/input.css -o ./static/output.css --minify

# Collect static files
RUN poetry run python manage.py collectstatic --noinput

# Make the startup script executable
RUN chmod 755 /code/start-django.sh

EXPOSE 8000

ENTRYPOINT ["/code/start-django.sh"]