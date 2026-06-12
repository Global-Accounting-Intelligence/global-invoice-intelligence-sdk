import httpx


class GlobalInvoiceIntelligenceClient:
    def __init__(self, base_url: str, api_key: str, tenant_id: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.tenant_id = tenant_id

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "X-Tenant-ID": self.tenant_id,
        }

    def match_invoice(self, payload: dict) -> dict:
        with httpx.Client(timeout=30) as client:
            response = client.post(
                f"{self.base_url}/v1/invoices/match",
                json=payload,
                headers=self._headers(),
            )
            response.raise_for_status()
            return response.json()

    def send_feedback(self, payload: dict) -> dict:
        with httpx.Client(timeout=30) as client:
            response = client.post(
                f"{self.base_url}/v1/feedback/correction",
                json=payload,
                headers=self._headers(),
            )
            response.raise_for_status()
            return response.json()
