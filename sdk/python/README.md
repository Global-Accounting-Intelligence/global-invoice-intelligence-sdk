# Python SDK

## Install

This is a starter SDK. Package publishing is not configured yet.

## Example

```python
from global_invoice_intelligence import GlobalInvoiceIntelligenceClient

client = GlobalInvoiceIntelligenceClient(
    base_url="https://api.example.com",
    api_key="YOUR_API_KEY",
    tenant_id="tenant_demo",
)

result = client.match_invoice(payload)
```
