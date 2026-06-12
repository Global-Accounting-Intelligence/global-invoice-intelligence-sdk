import json
from pathlib import Path

invoice = json.loads(Path("examples/invoices/invoice_normalized.json").read_text(encoding="utf-8"))
assert "invoice_id" in invoice
assert "lines" in invoice
print("Invoice example basic validation passed.")
