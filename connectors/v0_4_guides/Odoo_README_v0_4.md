# Odoo Connector

## Purpose

Use Odoo External API where applicable. MVP should create draft vendor bill only. Do not post automatically.

## MVP Rules

- Do not auto-post accounting documents.
- Create draft documents only where supported.
- Send item/material master data to GAI.
- Send supplier/company master data to GAI.
- Send PO data only when available.
- Receive material match results with reason, confidence, color, and recommendations.
- Send user feedback back to GAI.

## Required Data Exchange

Inbound to GAI:

- invoice file or payload,
- item/material master,
- supplier/company master,
- optional PO/GRN data,
- user feedback.

Outbound from GAI:

- normalized invoice,
- material match results,
- supplier match results,
- quality scores,
- draft creation payload,
- recommended master-data improvements.
