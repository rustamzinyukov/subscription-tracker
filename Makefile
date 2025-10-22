# Subscription Tracker - Development Makefile

.PHONY: help install dev test clean docker-build docker-up docker-down railway-setup railway-deploy

# Default target
help:
	@echo "🚀 Subscription Tracker - Available commands:"
	@echo ""
	@echo "📦 Setup:"
	@echo "  install          Install Python dependencies"
	@echo "  init-db          Initialize database with sample data"
	@echo ""
	@echo "🔧 Development:"
	@echo "  dev              Start development server"
	@echo "  test             Run tests"
	@echo "  clean            Clean up temporary files"
	@echo ""
	@echo "🐳 Docker:"
	@echo "  docker-build    Build Docker image"
	@echo "  docker-up       Start services with Docker Compose"
	@echo "  docker-down     Stop Docker services"
	@echo "  docker-init     Initialize database in Docker"
	@echo ""
	@echo "🚂 Railway:"
	@echo "  railway-setup    Setup Railway project"
	@echo "  railway-deploy   Deploy to Railway"
	@echo ""

# Python setup
install:
	@echo "📦 Installing Python dependencies..."
	cd backend && pip install -r requirements.txt

# Database setup
init-db:
	@echo "🗄️ Initializing database..."
	cd backend && python init_db.py

# Development server
dev:
	@echo "🚀 Starting development server..."
	cd backend && python run.py

# Testing
test:
	@echo "🧪 Running tests..."
	cd backend && python -m pytest tests/ -v

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t subscription-tracker .

docker-up:
	@echo "🐳 Starting services with Docker Compose..."
	docker-compose up -d

docker-down:
	@echo "🐳 Stopping Docker services..."
	docker-compose down

docker-init:
	@echo "🐳 Initializing database in Docker..."
	docker-compose --profile init up db-init

# Railway commands
railway-setup:
	@echo "🚂 Setting up Railway project..."
	chmod +x scripts/setup-railway.sh
	./scripts/setup-railway.sh

railway-deploy:
	@echo "🚂 Deploying to Railway..."
	chmod +x scripts/deploy.sh
	./scripts/deploy.sh

# Full development setup
setup: install init-db
	@echo "✅ Development environment ready!"
	@echo "🚀 Run 'make dev' to start the server"
