.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync --all-groups
	@uv run pre-commit install --hook-type commit-msg --hook-type pre-push

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
	@cd infra/terraform && terraform init -upgrade -backend-config="backend/local.gcs.backend"

.PHONY:	plan_terraform_local
plan_terraform_local:
	@terraform -chdir=infra/terraform plan -var-file="tfvars/local.tfvars"

.PHONY:	apply_terraform_local
apply_terraform_local:
	@terraform -chdir=infra/terraform apply -var-file="tfvars/local.tfvars" --auto-approve

.PHONY:	destroy_terraform_local
destroy_terraform_local:
	@terraform -chdir=infra/terraform destroy -var-file="tfvars/local.tfvars" --auto-approve

.PHONY: generate_key_iam
generate_key_iam:
	@bash deploy_service_account_CICD.sh

.PHONY: connect_gke_cli
connect_gke_cli:
	@gcloud container clusters get-credentials template-gke-cluster --region europe-west1 --project dataascode

.PHONY: apply_k8s
apply_k8s:
	@kubectl apply -f infra/k8s

.PHONY: delete_k8s
delete_k8s:
	@kubectl delete -f infra/k8s

.PHONY: helm_manifest
helm_manifest:
	helm get manifest event-driven-api > trash.log


.PHONY: helm_update_prod
helm_update_prod:
	helm upgrade --install event-driven-api infra/helm \
	--namespace default \
	--create-namespace \
	--values infra/helm/values.yaml

.PHONY: check_domain
check_domain:
	@gcloud domains registrations describe templatejojotest.com
	@gcloud domains registrations describe templatejojotest.com --format="yaml(dnsSettings.customDns.nameServers)" # To modify
	@gcloud dns managed-zones describe template-dns --project=dataascode --format="value(nameServers)" # Real one

.PHONY: fix_nameservers_developer
fix_nameservers_developer:
	@gcloud domains registrations configure dns templatejojotest.com \
		--name-servers="ns-cloud-d1.googledomains.com,ns-cloud-d2.googledomains.com,ns-cloud-d3.googledomains.com,ns-cloud-d4.googledomains.com"
.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.PHONY: docker_compose_up
docker_compose_up:
	docker compose up --build

.PHONY: locust_load_test_local
locust_load_test_local:
	uv run locust -f scripts/locustfile.py --host=http://localhost:8000


.PHONY: locust_load_test_prod
locust_load_test_prod:
	uv run locust -f scripts/locustfile.py --host=https://templatejojotest.com

.DEFAULT_GOAL := help
