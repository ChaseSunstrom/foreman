# Foreman observability (Claude Code → OpenTelemetry → telegraf → InfluxDB → Grafana)

Nothing here is active until you turn it on. Foreman never edits your telegraf config or enables telemetry on its own.

## 1. Telegraf
Append `telegraf.conf` (an `inputs.opentelemetry` listener on :4317, tagged `source=claude-code`) to your telegraf config, route it to a bucket (example output block included, commented out), and restart telegraf.

## 2. Claude Code
Add to `~/.claude/settings.json` (user scope: project/local settings can't turn telemetry on), then restart Claude Code:
```json
"env": {
  "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
  "OTEL_METRICS_EXPORTER": "otlp",
  "OTEL_LOGS_EXPORTER": "otlp",
  "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
  "OTEL_EXPORTER_OTLP_ENDPOINT": "http://<telegraf-host>:4317",
  "OTEL_METRIC_EXPORT_INTERVAL": "10000"
}
```
Keep content logging off (the defaults): don't set `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_ASSISTANT_RESPONSES`, `OTEL_LOG_TOOL_DETAILS`, `OTEL_LOG_TOOL_CONTENT` or `OTEL_LOG_RAW_API_BODIES`.

Metrics exported (docs: monitoring-usage): `claude_code.session.count`, `.cost.usage`, `.token.usage` (by type: input/output/cacheRead/cacheCreation, and by model), `.lines_of_code.count`, `.commit.count`, `.pull_request.count`, `.code_edit_tool.decision`, `.active_time.total`. Events (logs): tool results with durations, API requests, permission decisions.

## 3. Grafana
Import `grafana-dashboard.json` and pick your InfluxDB (Flux) datasource and bucket. The queries match fields by regex (`/claude_code_cost_usage/` etc.) because telegraf's field names depend on its schema and version; check yours with
`from(bucket: "claude") |> range(start: -1h) |> keep(columns: ["_field"]) |> distinct(column: "_field")` and adjust if needed.

Local, zero-setup alternative: `fm watch` (tool timeline, hook latency, session cost and context from the statusline snapshot).
