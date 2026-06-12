# Getting Started

## Steps

1. Obtain API URL and API key.
2. Prepare normalized invoice JSON.
3. Send invoice to `/v1/invoices/match`.
4. Receive match results.
5. Send user feedback to `/v1/feedback/correction`.

## Headers

- `Authorization: Bearer <api_key>`
- `X-Tenant-ID: <tenant_id>`
