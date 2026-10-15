---
name: serilog
title: Serilog
area: dotnet
tags: [dotnet, csharp, logging, structured, sinks, observability]
detect: [dep:Serilog, dep:Serilog.AspNetCore, dep:Serilog.Sinks.Console]
related: [aspnet-core, dotnet-aspire, xunit]
---
Serilog: structured logging with message templates, enrichers and sinks, configured once at startup and flushed at shutdown.

## Verify
- `dotnet build -warnaserror`: log call sites and configuration compile.
- `dotnet test --filter "FullyQualifiedName~Logging"`: tests capturing events through an in-memory sink pass.
- `grep -rnE "Log\.(Information|Warning|Error|Debug)\(\$\"" --include=*.cs .`: finds interpolated log messages, which should return nothing.

## Test first
Capture events with a test sink and assert on properties, not on rendered text.
```csharp
public class CollectingSink : ILogEventSink
{
    public List<LogEvent> Events { get; } = new();
    public void Emit(LogEvent e) => Events.Add(e);
}

[Fact]
public void Payment_failure_logs_order_id_as_property()
{
    var sink = new CollectingSink();
    var log = new LoggerConfiguration().WriteTo.Sink(sink).CreateLogger();
    new PaymentService(log).Fail(42);
    Assert.Equal("42", sink.Events.Single().Properties["OrderId"].ToString());
}
```

## Do
- Use `builder.Host.UseSerilog((ctx, lc) => lc.ReadFrom.Configuration(ctx.Configuration).Enrich.FromLogContext())` so levels and sinks live in `appsettings.json` under `Serilog`.
- Use `Log.Logger = new LoggerConfiguration()...CreateBootstrapLogger()` for startup errors, and finish with `try { ... } finally { Log.CloseAndFlush(); }`.
- Write message templates with named holes: `log.Information("Paid {OrderId} {Amount}", id, amount)`.
- Add `app.UseSerilogRequestLogging()` for one summary line per request, and place it after static files and before endpoints.
- Use `LogContext.PushProperty` or `BeginScope` for correlation ids, with `Enrich.FromLogContext()` enabled.
- Override noisy namespaces with `MinimumLevel.Override("Microsoft.AspNetCore", LogEventLevel.Warning)`.
- Use `{@Order}` to destructure objects deliberately and `Destructure.ByTransforming` to drop secrets.

## Avoid
- String interpolation or concatenation in log calls: it kills structure and allocates. Use templates with arguments.
- Logging whole request bodies, tokens or passwords with `{@...}`: use a destructuring policy to mask them.
- Skipping `Log.CloseAndFlush()`: buffered events are lost on exit, especially with async or network sinks.
- Passing an exception into the template, as in `Error("fail {Ex}", ex)`: use `Error(ex, "fail ...")` as the first argument.
- `Log.Logger` global calls in library code: inject `ILogger<T>` or `ILogger` instead.
- Debug level enabled globally in production: set it in configuration per environment.

## Review
- [ ] No interpolated or concatenated log messages, and property names are stable PascalCase.
- [ ] Configuration comes from settings, and `CloseAndFlush` runs on every exit path.
- [ ] No secrets or PII are logged, and destructuring is explicit.
- [ ] Request logging is on, with correlation ids enriched.
- [ ] Noisy framework namespaces are overridden to Warning.
