# wiki-rag

Terraform + ECS Fargate pipeline that:
1) ingests Wikipedia content into S3
2) indexes into Postgres (pgvector) using embeddings
3) serves a FastAPI RAG API behind an ALB

This version adds a provider abstraction so the same RAG pipeline can switch between:
- OpenAI chat + OpenAI embeddings
- Claude on Amazon Bedrock + OpenAI embeddings
- Claude on Amazon Bedrock + Bedrock embeddings

The intended Part VII path is:
- keep ingestion, chunking, pgvector, and FastAPI unchanged
- swap answer generation from ChatGPT/OpenAI to Claude on Amazon Bedrock
- optionally reindex later with Bedrock embeddings for a fully AWS-native model layer

## Prereqs

- Terraform >= 1.6
- AWS CLI configured for the target account
- jq
- psql (optional, for DB inspection)

## 1) Secrets (required)

Create a Secrets Manager secret named:

wiki-rag/app

SecretString can contain the OpenAI key if you still use OpenAI embeddings, or omit it if you are fully on Bedrock.

```json
{
  "DB_PASSWORD": "your-db-password"
}
```

## 2) Core runtime configuration

### Minimal Part VII setup: Claude on Bedrock for generation, OpenAI for embeddings

```bash
export LLM_PROVIDER=bedrock
export EMBEDDING_PROVIDER=openai
export AWS_REGION=ap-southeast-2
export BEDROCK_CHAT_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
export OPENAI_EMBED_MODEL=text-embedding-3-small
export EMBED_DIM=1536
```

### Optional fully AWS-native model layer: Claude + Bedrock embeddings

```bash
export LLM_PROVIDER=bedrock
export EMBEDDING_PROVIDER=bedrock
export AWS_REGION=ap-southeast-2
export BEDROCK_CHAT_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
export BEDROCK_EMBED_MODEL_ID=amazon.titan-embed-g1-text-02
export EMBED_DIM=1536
```

If you switch embedding providers or embedding dimensions, re-run the indexer so the vectors stored in pgvector match the query-time embedding model.

## 3) Stand up infra

From terraform/:

```bash
terraform init
terraform apply
```

## 4) Deploy containers (push images)

ECS task defs reference `:latest`, so you must push images before tasks can start.

Use GitHub Actions workflows:

- deploy-api
- deploy-ingest
- deploy-indexer

Verify API service is running:

```bash
REGION=ap-southeast-2
CLUSTER=wiki-rag
SERVICE=wiki-rag-api

aws ecs describe-services --cluster "$CLUSTER" --services "$SERVICE" --query 'services[0].{desired:desiredCount,running:runningCount,taskDef:taskDefinition}' --output table
```

Healthcheck:

```bash
ALB=$(terraform output -raw api_url)
curl -i "$ALB/health"
```

## 5) Bootstrap data (first run)

Scheduled EventBridge runs will eventually populate the system, but for a fresh environment do:

1) Run ingest once
2) Run indexer once

### Run ingest

```bash
bash scripts/run_ingest.sh
```

### Run indexer

```bash
bash scripts/run_indexer.sh
```

## 6) Test the API

```bash
ALB=$(terraform output -raw api_url)
curl -sS -i -H "Content-Type: application/json" \
  -d '{"question":"What documents were indexed?"}' \
  "$ALB/ask"
```

Expected: `HTTP/1.1 200 OK` with answer + evidence.

## Notes on the provider split

### What changes with Bedrock
- the answer-generation provider
- AWS identity and IAM permissions for model invocation
- model ID and region configuration
- optional embedding provider if you choose to reindex with Bedrock embeddings

### What stays the same
- S3 ingestion pipeline
- document chunking flow
- pgvector as the vector store
- FastAPI API contract
- retrieval shape and evidence handling

## Tear down

Terraform destroy will fail if:

- ECR repos are not empty
- S3 buckets contain objects

Run cleanup scripts first if needed, then:

```bash
terraform destroy
```

## License

MIT.
