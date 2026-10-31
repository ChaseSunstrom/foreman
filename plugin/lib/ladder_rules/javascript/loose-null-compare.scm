; kind: bug
; message: == against a literal coerces types; use ===
(binary_expression operator: ["==" "!="] right: [(number) (string) (true) (false)]) @m
