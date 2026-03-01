resource "aws_ecs_task_definition" "ingest" {
  family                   = "${local.project}-ingest"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = aws_iam_role.task_execution.arn
  task_role_arn            = aws_iam_role.task_role.arn

  container_definitions = jsonencode([{
    name      = "ingest"
    image     = "${aws_ecr_repository.ingest.repository_url}:latest"
    essential = true
    environment = [
      { name = "RAW_BUCKET", value = aws_s3_bucket.raw.bucket },
      { name = "PARSED_BUCKET", value = aws_s3_bucket.parsed.bucket },
      { name = "DB_HOST", value = aws_db_instance.postgres.address },
      { name = "DB_PORT", value = "5432" },
      { name = "DB_NAME", value = "postgres" },
      { name = "DB_USER", value = var.db_username }
    ]
    secrets = [
      { name = "DB_PASSWORD", valueFrom = "${data.aws_secretsmanager_secret.app.arn}:DB_PASSWORD::" },
      { name = "OPENAI_API_KEY", valueFrom = "${data.aws_secretsmanager_secret.app.arn}:OPENAI_API_KEY::" }
    ]
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        awslogs-group         = aws_cloudwatch_log_group.ingest.name,
        awslogs-region        = local.aws_region,
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

resource "aws_iam_role" "events_run_task" {
  name = "${local.project}-events-run-task"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "events.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "events_run_task" {
  role = aws_iam_role.events_run_task.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Action    = ["ecs:RunTask"],
        Resource  = [
          aws_ecs_task_definition.ingest.arn,
          aws_ecs_task_definition.indexer.arn
        ],
        Condition = { ArnLike = { "ecs:cluster" = aws_ecs_cluster.this.arn } }
      },
      {
        Effect   = "Allow",
        Action   = ["iam:PassRole"],
        Resource = [aws_iam_role.task_execution.arn, aws_iam_role.task_role.arn]
      }
    ]
  })
}

resource "aws_cloudwatch_event_rule" "ingest_schedule" {
  name                = "${local.project}-ingest"
  description         = "Scheduled ingest"
  schedule_expression = "rate(6 hours)"
}

resource "aws_cloudwatch_event_target" "ingest" {
  rule      = aws_cloudwatch_event_rule.ingest_schedule.name
  target_id = "ecs-ingest"
  arn       = aws_ecs_cluster.this.arn
  role_arn  = aws_iam_role.events_run_task.arn

  ecs_target {
    task_definition_arn = aws_ecs_task_definition.ingest.arn
    launch_type         = "FARGATE"
    network_configuration {
      subnets          = aws_subnet.private[*].id
      security_groups  = [aws_security_group.ecs_tasks.id]
      assign_public_ip = false
    }
  }
}

resource "aws_cloudwatch_event_rule" "indexer_schedule" {
  name                = "${local.project}-indexer"
  description         = "Scheduled index rebuild"
  schedule_expression = "rate(12 hours)"
}

resource "aws_cloudwatch_event_target" "indexer" {
  rule      = aws_cloudwatch_event_rule.indexer_schedule.name
  target_id = "ecs-indexer"
  arn       = aws_ecs_cluster.this.arn
  role_arn  = aws_iam_role.events_run_task.arn

  ecs_target {
    task_definition_arn = aws_ecs_task_definition.indexer.arn
    launch_type         = "FARGATE"
    network_configuration {
      subnets          = aws_subnet.private[*].id
      security_groups  = [aws_security_group.ecs_tasks.id]
      assign_public_ip = false
    }
  }
}
