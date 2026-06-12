# API Overview

## Core Endpoints

- `POST /v1/invoices/normalize`
- `POST /v1/invoices/match`
- `GET /v1/invoices/{id}/result`
- `POST /v1/feedback/correction`
- `GET /v1/materials/{id}/score`

## Response Philosophy

Every match should include:

- confidence
- status color
- explanation
- evidence
- improvement suggestions
