---
name: xxe
title: XML external entities
area: security
tags: [security, xxe, xml, parser, dtd, ssrf]
detect: [dep:defusedxml, dep:lxml]
related: [ssrf, saml, upload-security, unsafe-deserialization, path-traversal]
---
Parse untrusted XML with DTDs, external entities and network access off; prefer JSON, and treat SVG, DOCX and SAML as XML.

## Verify
- `git grep -nE "etree|DocumentBuilder|SAXParser|XMLReader|simplexml|xml2js|libxmljs" -- ':!*test*'`: every XML parse site is found.
- `python -c "import defusedxml.ElementTree as E; E.fromstring('<!DOCTYPE a [<!ENTITY x SYSTEM \"file:///etc/hostname\">]><a>&x;</a>')"`: defusedxml raises instead of resolving the entity.
- `pytest -q -k xxe`: the regression test below passes.

## Test first
Feed a document that declares a harmless local entity, and require rejection.
```python
import pytest

DOC = b'<?xml version="1.0"?><!DOCTYPE r [<!ENTITY e SYSTEM "file:///etc/hostname">]><r>&e;</r>'

def test_upload_xml_with_entity_is_rejected(client):
    r = client.post("/import", files={"f": ("a.xml", DOC, "text/xml")})
    assert r.status_code == 400
    assert "localhost" not in r.text
```

## Do
- Python: use `defusedxml`, or `lxml` with `resolve_entities=False, no_network=True, load_dtd=False`.
- Java: set `disallow-doctype-decl` true on the factory. If DTDs are required, disable external general and parameter entities and `FEATURE_SECURE_PROCESSING` on top.
- .NET: `DtdProcessing.Prohibit` and `XmlResolver = null`.
- Node: choose parsers that do not expand entities, and reject documents containing `<!DOCTYPE`.
- Cap the document size and nesting depth to limit billion-laughs expansion.
- Check XML-bearing formats: SVG, Office files, SOAP, SAML, RSS, sitemap.
- Run the parser with no egress and no sensitive file access where possible.

## Avoid
- Default `DocumentBuilderFactory`, `SAXParserFactory` or `XMLInputFactory`: most are unsafe until configured. Set the flags explicitly.
- `lxml.etree.XMLParser()` defaults on untrusted input: pass the hardened options.
- Only blocking `SYSTEM`: parameter entities and `PUBLIC` also load. Disable the DTD entirely.
- Sanitising by regex on `<!ENTITY`: encodings bypass it. Configure the parser.
- Rendering uploaded SVG server-side with a resolver that fetches URLs: disable external loading.
- Returning the parser error text to users: it can include file content.

## Review
- [ ] Every parser instance is configured safe, shared through one helper.
- [ ] DOCTYPE is rejected or entity resolution is disabled and tested.
- [ ] Size and depth limits exist.
- [ ] Indirect XML (SVG, DOCX, SAML) is covered.
- [ ] Error responses do not leak parsed content.
