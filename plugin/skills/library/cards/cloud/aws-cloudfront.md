---
name: aws-cloudfront
title: AWS CloudFront
area: cloud
tags: [aws, cloudfront, cdn, cache, oac, invalidation, edge]
detect: [dep:@aws-sdk/client-cloudfront, dep:@aws-sdk/cloudfront-signer]
related: [aws-s3, aws-cdk, aws-api-gateway, aws-iam, aws-cloudformation]
---
CloudFront distributions: private S3 origins through Origin Access Control, explicit cache policies, HTTPS only, versioned assets instead of invalidations.

## Verify
- `aws cloudfront get-distribution-config --id ID --query 'DistributionConfig.[DefaultCacheBehavior.ViewerProtocolPolicy,Origins.Items[].OriginAccessControlId]'`: HTTPS is enforced and OAC is attached.
- `curl -sI https://DOMAIN/asset.js`: check `x-cache`, `cache-control` and `age` headers.
- `curl -sI https://BUCKET.s3.REGION.amazonaws.com/asset.js`: direct S3 access returns 403.
- `aws cloudfront create-invalidation --distribution-id ID --paths '/index.html'`: a targeted invalidation, only when needed.

## Test first
Write a smoke test for the cache and for the origin lock before the distribution config.
```python
def test_assets_cached_and_s3_private(cdn, s3_url):
    cdn.get("/app.abc123.js"); r = cdn.get("/app.abc123.js")
    assert r.headers["x-cache"].startswith("Hit")
    assert requests.get(s3_url + "/app.abc123.js").status_code == 403
```

## Do
- Use Origin Access Control for S3 and a bucket policy that allows only `cloudfront.amazonaws.com` with an `AWS:SourceArn` condition for the distribution.
- Use managed cache and origin-request policies, or define them explicitly. Forward only the headers, cookies and query strings the origin needs, because every extra one splits the cache.
- Hash asset file names and send `Cache-Control: max-age=31536000, immutable`. Send `no-cache` for `index.html`.
- Set `viewer-protocol-policy` to `redirect-to-https` and a modern minimum TLS policy. The ACM certificate for CloudFront must be in us-east-1.
- Map SPA routes with custom error responses (403 and 404 to `/index.html` with 200) only for SPAs.
- Add a response headers policy for HSTS, `X-Content-Type-Options` and CSP.
- Use signed URLs or cookies with a trusted key group for private content.
- Enable standard logs or real-time logs for debugging, and attach WAF where traffic is public.

## Avoid
- Legacy Origin Access Identity for new work: use OAC.
- A public S3 bucket behind CloudFront: bypasses WAF and signing. Block public access.
- Forwarding all cookies and headers: cache hit ratio drops to near zero. Use an allow-list.
- Invalidating `/*` on every deploy: it is slow and costs money past the free quota. Version file names.
- Certificate created outside us-east-1: it will not attach.
- Caching authenticated responses: set `Cache-Control: private` or `no-store` and exclude them from the behavior.
- Missing `Vary` handling on compressed content: enable compression in the cache policy instead of at the origin.

## Review
- [ ] Origin is private and reachable only through the distribution.
- [ ] Cache keys include only needed headers, cookies and queries.
- [ ] Static assets are fingerprinted, HTML is not cached long.
- [ ] HTTPS and security headers enforced.
- [ ] Deploy script does not blanket-invalidate.
