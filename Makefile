.PHONY: lint

lint:
	shellcheck scripts/deploy_ingest.sh
