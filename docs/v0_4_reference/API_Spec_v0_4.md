# API Specification — Global Accounting Intelligence
## Version 0.3

# 1. API Principles

1. REST-first.
2. JSON responses.
3. Versioned endpoints under `/v1`.
4. Idempotency support for create operations.
5. Signed webhooks.
6. Tenant-scoped API keys.
7. Sandbox and production separation.
8. Every intelligence output includes confidence and evidence where applicable.

# 2. Authentication

Header:

```http
Authorization: Bearer <api_key>
X-Tenant-ID: <tenant_id>
Idempotency-Key: <unique_key>
```

# 3. Core Endpoints

## 3.1 Submit Invoice

`POST /v1/invoices`

Use for PDF/image/XML/JSON/API invoice submission.

Input modes:

- multipart file,
- JSON payload,
- QR payload,
- structured invoice object,
- optional PO/GRN signals.

Response:

```json
{
  "invoice_id": "inv_123",
  "status": "processing",
  "source_type": "pdf",
  "created_at": "2026-06-12T12:00:00Z"
}
```

## 3.2 Get Invoice Result

`GET /v1/invoices/{invoice_id}`

Returns:

- normalized invoice,
- supplier match,
- material matches,
- quality scores,
- validation results,
- recommended actions.

## 3.3 Match Materials

`POST /v1/match/materials`

Purpose:

Compare invoice lines with customer item/material master.

Request:

```json
{
  "invoice_lines": [
    {
      "line_id": "1",
      "name": "HP 85A TONER BLACK",
      "supplier_item_code": "CE285A",
      "quantity": 2,
      "uom": "PCS",
      "unit_price": 18.5,
      "tax_rate": 16
    }
  ],
  "materials": [
    {
      "external_item_id": "ITEM-00452",
      "item_name": "HP LaserJet Toner 85A Black",
      "supplier_references": ["CE285A"],
      "uom": "PCS"
    }
  ],
  "supplier": {
    "name": "ABC Supplies",
    "tax_number": "123456789"
  },
  "purchase_order": null
}
```

Response must include:

- suggested material,
- confidence,
- color,
- reason,
- evidence,
- conflicts,
- material card improvements.

## 3.4 Score Materials

`POST /v1/quality/materials`

Scores item cards from 1 to 100.

## 3.5 Score Companies

`POST /v1/quality/companies`

Scores company/supplier cards from 1 to 100.

## 3.6 Score XML

`POST /v1/quality/xml`

Scores XML invoice quality from 1 to 100.

## 3.7 Submit Feedback

`POST /v1/feedback/matches`

Used by connectors and UI after user approves, rejects, or corrects a suggestion.

Request:

```json
{
  "match_result_id": "mmr_123",
  "action": "corrected",
  "selected_material_id": "ITEM-00999",
  "reason": "User confirmed this supplier always uses this description for ITEM-00999."
}
```

# 4. Connector Endpoints

## 4.1 Create ERP Draft Purchase Invoice

`POST /v1/connectors/{connector}/draft-purchase-invoice`

Supported connectors in early stages:

- `erpnext`
- `odoo`
- `tallyprime`
- `quickbooks` if supported
- `generic_rest`

MVP behavior:

- create draft only,
- no automatic posting,
- return ERP draft ID.

# 5. Webhooks

Events:

- `invoice.received`
- `invoice.processed`
- `invoice.failed`
- `invoice.requires_review`
- `invoice.ready_for_draft`
- `material.match_completed`
- `material.match_approved`
- `material.match_rejected`
- `quality.report_completed`
- `erp.draft_created`

Webhook security:

- signed payload,
- timestamp,
- replay protection,
- retry policy,
- delivery logs.

# 6. Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invoice total does not match line totals.",
    "details": [
      {
        "field": "totals.payable_amount",
        "expected": 100.0,
        "actual": 98.5
      }
    ]
  },
  "request_id": "req_123"
}
```
