# Property Agency Ecosystem - Deployment Makefile

.PHONY: help build up down logs clean dev prod status health

# Default target
help:
	@echo "Property Agency Ecosystem - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start development environment"
	@echo "  make dev-logs     - View development logs"
	@echo "  make dev-down     - Stop development environment"
	@echo ""
	@echo "Production:"
	@echo "  make build        - Build all Docker images"
	@echo "  make up           - Start production environment"
	@echo "  make down         - Stop production environment"
	@echo "  make prod         - Build and start production environment"
	@echo ""
	@echo "Monitoring:"
	@echo "  make logs         - View production logs"
	@echo "  make status       - Check service status"
	@echo "  make health       - Check health of all services"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        - Clean up Docker resources"
	@echo "  make restart      - Restart all services"
	@echo "  make update       - Update and restart services"

# Development environment
dev:
	@echo "Starting development environment..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "Development environment started at http://localhost:3000"

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev-down:
	docker-compose -f docker-compose.dev.yml down

# Production environment
build:
	@echo "Building Docker images..."
	docker-compose build --no-cache

up:
	@echo "Starting production environment..."
	docker-compose up -d
	@echo "Production environment started at http://localhost"

down:
	docker-compose down

prod: build up
	@echo "Production environment is ready!"

# Monitoring
logs:
	docker-compose logs -f

status:
	docker-compose ps

health:
	@echo "Checking service health..."
	@curl -s http://localhost/health || echo "Web app: DOWN"
	@curl -s http://localhost:5001/health || echo "CRM service: DOWN"
	@curl -s http://localhost:5002/health || echo "Analytics service: DOWN"
	@curl -s http://localhost:5003/health || echo "AI enrichment: DOWN"
	@curl -s http://localhost:5004/health || echo "28Hse scraper: DOWN"
	@curl -s http://localhost:5005/health || echo "Squarefoot scraper: DOWN"

# Maintenance
clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f
	docker volume prune -f

restart:
	docker-compose restart

update:
	@echo "Updating services..."
	git pull
	docker-compose build --no-cache
	docker-compose up -d
	@echo "Services updated and restarted!"

# Database operations
db-backup:
	@echo "Backing up databases..."
	docker-compose exec crm-service sqlite3 /app/src/database/crm.db ".backup /app/backup-crm-$(shell date +%Y%m%d_%H%M%S).db"
	docker-compose exec analytics-service sqlite3 /app/src/database/analytics.db ".backup /app/backup-analytics-$(shell date +%Y%m%d_%H%M%S).db"

db-restore:
	@echo "Database restore requires manual intervention. Check documentation."

# SSL certificate generation (for production)
ssl-cert:
	@echo "Generating self-signed SSL certificate..."
	mkdir -p ssl
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout ssl/key.pem \
		-out ssl/cert.pem \
		-subj "/C=HK/ST=Hong Kong/L=Hong Kong/O=Property Agency/CN=localhost"

# Environment setup
setup:
	@echo "Setting up environment..."
	cp .env.example .env
	@echo "Please edit .env file with your configuration"
	@echo "Then run: make ssl-cert && make prod"

