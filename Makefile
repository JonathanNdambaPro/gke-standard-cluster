.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
	@uv run pre-commit install --hook-type commit-msg

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running ty"
	@uv run ty check
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@uv run deptry .

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: publish
publish: ## Publish a release to PyPI.
	@echo "🚀 Publishing."
	@uvx twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish.

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@uv run mkdocs serve

.PHONY:	init_terraform_local
init_terraform_local:
	@cd infra/terraform && terraform init -upgrade -backend-config="infra/terraform/local.gcs.backend"

.PHONY:	plan_terraform_local
plan_terraform_local:
	@terraform -chdir=infra/terraform plan -var-file="tfvars/local.tfvars"

.PHONY:	apply_terraform_local
apply_terraform_local:
	@terraform -chdir=infra/terraform apply -var-file="tfvars/local.tfvars" --auto-approve

.PHONY: generate_key_iam
generate_key_iam:
	bash deploy_service_account_CICD.sh

.PHONY: connect_gke_cli
connect_gke_cli:
	@gcloud container clusters get-credentials template-gke-cluster --region europe-west1 --project dataascode

.PHONY: apply_k8s
apply_k8s:
	@kubectl apply -f infra/k8s

.PHONY: delete_k8s
delete_k8s:
	@kubectl delete -f infra/k8s

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
