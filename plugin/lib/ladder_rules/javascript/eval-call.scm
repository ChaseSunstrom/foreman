; kind: vuln
; message: eval runs a string as code
(call_expression function: (identifier) @f (#eq? @f "eval")) @m
