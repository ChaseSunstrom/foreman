---
name: signalr
title: ASP.NET Core SignalR
area: dotnet
tags: [dotnet, csharp, signalr, realtime, websockets, hubs]
detect: [dep:Microsoft.AspNetCore.SignalR.Client, dep:Microsoft.AspNetCore.SignalR.StackExchangeRedis, dep:Microsoft.AspNetCore.SignalR.Protocols.MessagePack]
related: [aspnet-core, blazor, xunit, dotnet-cli]
---
SignalR: server hubs, strongly typed clients, groups, auth, scale-out and client reconnects.

## Verify
- `dotnet build -warnaserror`: compiles clean.
- `dotnet test`: hub tests, including a real client against the test server.
- `dotnet list package --vulnerable`: no vulnerable transitive packages.
- `dotnet format --verify-no-changes`: formatting.

## Test first
Connect a `HubConnection` to `WebApplicationFactory<Program>` using its handler for the transport.
```csharp
[Fact]
public async Task Send_broadcasts_to_clients()
{
    var tcs = new TaskCompletionSource<string>();
    var conn = new HubConnectionBuilder()
        .WithUrl("http://localhost/chat", o =>
            o.HttpMessageHandlerFactory = _ => factory.Server.CreateHandler())
        .Build();
    conn.On<string>("Receive", m => tcs.TrySetResult(m));
    await conn.StartAsync();
    await conn.InvokeAsync("Send", "hi");
    Assert.Equal("hi", await tcs.Task.WaitAsync(TimeSpan.FromSeconds(5)));
}
```

## Do
- Map hubs with `app.MapHub<ChatHub>("/chat")` and call `AddSignalR()`.
- Use `Hub<IChatClient>` for strongly typed client calls instead of magic strings.
- Require auth with `[Authorize]` on the hub; for browser WebSockets read the token from the `access_token` query string in `JwtBearerEvents.OnMessageReceived`, only for the hub path.
- Push from outside hubs through `IHubContext<THub, TClient>`.
- Use groups (`Groups.AddToGroupAsync`) for rooms; remember membership is not persisted across reconnects, so re-add on connect.
- Configure the client with `WithAutomaticReconnect()` and handle `Reconnecting`, `Reconnected` and `Closed`.
- Add a Redis backplane (`AddStackExchangeRedis`) or Azure SignalR when running more than one server.

## Avoid
- Storing per-connection state in hub fields: a hub instance exists per call. Use a keyed store.
- Treating connection IDs as user IDs: a user has many connections and the ID changes on reconnect. Use `Clients.User(userId)` with a user identifier provider.
- Putting the access token in the query string for all endpoints: it leaks into logs. Limit to the hub path.
- Long-running work inside a hub method: it blocks that connection's message processing. Queue it.
- `.Result` on `InvokeAsync`: deadlocks. Await.
- Multiple servers without sticky sessions or a backplane: messages reach only local clients.
- Permissive CORS with credentials for the hub: list explicit origins.

## Review
- [ ] Hub and methods are authorized; groups checked against the user's rights.
- [ ] Clients reconnect and rebuild group and subscription state.
- [ ] Typed hubs, no stringly named methods.
- [ ] Scale-out path (backplane) is decided for multi-instance deployment.
- [ ] Test uses a real client, with a timeout on every wait.
