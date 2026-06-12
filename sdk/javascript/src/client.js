export class GlobalInvoiceIntelligenceClient {
  constructor({ baseUrl, apiKey, tenantId }) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.apiKey = apiKey;
    this.tenantId = tenantId;
  }

  headers() {
    return {
      'Authorization': `Bearer ${this.apiKey}`,
      'X-Tenant-ID': this.tenantId,
      'Content-Type': 'application/json'
    };
  }

  async matchInvoice(payload) {
    const response = await fetch(`${this.baseUrl}/v1/invoices/match`, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return response.json();
  }
}
