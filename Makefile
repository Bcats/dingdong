# Makefile for notification-platform

.PHONY: help install dev-install up down restart logs clean test format lint

# 默认目标
.DEFAULT_GOAL := help

help: ## 显示帮助信息
	@echo "可用命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## 安装生产依赖
	pip install -r requirements.txt

dev-install: ## 安装开发依赖
	pip install -r requirements-dev.txt
	pre-commit install

up: ## 启动所有服务
	docker-compose up -d

down: ## 停止所有服务
	docker-compose down

restart: ## 重启所有服务
	docker-compose restart

logs: ## 查看日志
	docker-compose logs -f

clean: ## 清理临时文件
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage htmlcov
	rm -rf dist build

test: ## 运行测试
	pytest

test-cov: ## 运行测试并生成覆盖率报告
	pytest --cov=app --cov-report=html --cov-report=term

format: ## 格式化代码
	black app
	isort app

lint: ## 代码检查
	flake8 app
	pylint app
	mypy app

migrate: ## 运行数据库迁移
	docker-compose exec api alembic upgrade head

migrate-create: ## 创建新的迁移文件
	docker-compose exec api alembic revision --autogenerate -m "$(message)"

api-key: ## 创建API密钥
	docker-compose exec api python scripts/create_api_key.py --name "$(name)"

email-account: ## 添加邮箱账户
	docker-compose exec api python scripts/add_email_account.py \
		--email $(email) \
		--smtp-host $(host) \
		--smtp-port $(port) \
		--smtp-username $(username) \
		--smtp-password $(password)

shell: ## 进入API容器shell
	docker-compose exec api bash

db-shell: ## 进入数据库shell
	docker-compose exec postgres psql -U notification_user -d notification_db

backup: ## 备份数据库
	docker-compose exec postgres pg_dump -U notification_user notification_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

init: ## 初始化项目（首次使用）
	@echo "初始化项目..."
	cp .env.example .env
	@echo "✅ 已创建.env文件，请编辑配置"
	@echo "📝 接下来执行:"
	@echo "  1. 编辑.env文件，设置密码和密钥"
	@echo "  2. make up - 启动服务"
	@echo "  3. make migrate - 运行数据库迁移"
	@echo "  4. make api-key name='我的密钥' - 创建API密钥"

