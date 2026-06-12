import { GlobalInvoiceIntelligenceClient } from '../src/index.js';

const client = new GlobalInvoiceIntelligenceClient({
  baseUrl: 'https://api.example.com',
  apiKey: 'test',
  tenantId: 'tenant_demo'
});

console.log(Boolean(client));
