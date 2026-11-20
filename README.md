# Prompt injection test page

A static test page for an article on indirect prompt injection in scraping agents.

The page looks like a normal product page for a fictional store. It also hides 14 harmless
payloads, one per concealment technique (hidden elements, HTML comments, zero-width characters,
`alt` and `title` attributes, a `<meta>` tag, external CSS, JavaScript cloaking and plain visible text).
Each payload only asks a model to print a canary string such as `CANARY-7F3A-01` or to call a fake
`send_email` tool addressed to `attacker@example.com` (a reserved domain that can't receive mail).

Use it only to test your own pipelines. Don't copy these payloads onto sites you don't own.
