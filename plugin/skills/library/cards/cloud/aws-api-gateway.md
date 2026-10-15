---
name: aws-api-gateway
title: AWS API Gateway
area: cloud
tags: [aws, api-gateway, http-api, rest-api, authorizer, throttling, cors]
detect: [dep:@aws-sdk/client-api-gateway, dep:@aws-sdk/client-apigatewayv2, dep:@aws-sdk/client-apigatewaymanagementapi]
related: [aws-lambda, aws-cognito, aws-cloudfront, aws-iam, aws-sam]
---
API Gateway HTTP and REST APIs: an authorizer on every route, throttles, tight CORS, access logs, and payload and timeout limits respected.

## Verify
- `aws apigatewayv2 get-routes --api-id ID --query 'Items[].[RouteKey,AuthorizationType]'`: no route is unintentionally NONE (HTTP API).
- `aws apigateway get-stages --rest-api-id ID --query 'item[].[stageName,accessLogSettings,methodSettings]'`: stage has access logs and throttling (REST API).
- `curl -si https://ID.execute-api.REGION.amazonaws.com/path`: unauthenticated call gets 401 or 403.
- `curl -si -X OPTIONS -H 'Origin: https://app.example.com' -H 'Access-Control-Request-Method: GET' URL`: CORS preflight returns only the allowed origin.

## Test first
Write a smoke test that the route rejects a missing token and accepts a valid one.
```python
def test_orders_requires_token(base_url, token):
    assert requests.get(f"{base_url}/orders").status_code in (401, 403)
    r = requests.get(f"{base_url}/orders", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
```

## Do
- Choose HTTP API for plain proxying with JWT auth. Choose REST API only when you need usage plans, API keys, request validation or WAF.
- Attach an authorizer (JWT, Lambda or IAM) to every route. Make public routes explicit.
- Set stage throttling (`ThrottlingRateLimit`, `ThrottlingBurstLimit`) and per-route overrides for costly routes.
- Allow explicit CORS origins, methods and headers. Return CORS headers from Lambda too on REST proxy integrations.
- Enable access logs to CloudWatch with request id, status, latency and the integration error.
- Validate request bodies with a model on REST APIs, and again in the handler.
- Deploy through IaC with stage variables or aliases. Use canary or Lambda alias weights for rollouts.
- Use a custom domain with a regional certificate. Put WAF on REST APIs that face the internet.

## Avoid
- Missing authorizer on a route: it is public. Set `AuthorizationType` and test for 401.
- `Access-Control-Allow-Origin: *` with credentials, or reflecting any origin: pin the allowed list.
- Long handlers: the integration timeout is 29 seconds on REST by default and 30 seconds on HTTP. Move slow work behind a queue and return 202.
- Payloads past the 10 MB request limit: use S3 presigned URLs for uploads.
- Forgetting a redeploy on REST APIs: edits to resources do not go live until a new deployment is created to the stage.
- Lambda authorizer caching the wrong key: a result cached across users grants access wrongly. Key the cache on the token.
- Logging full request bodies: PII ends up in logs. Log ids and status only.

## Review
- [ ] Every route has an authorizer or a documented public reason.
- [ ] Throttling, access logs and CORS are set in IaC.
- [ ] Slow or large work is async.
- [ ] Authorizer cache key is correct.
- [ ] Custom domain and WAF considered for public APIs.
