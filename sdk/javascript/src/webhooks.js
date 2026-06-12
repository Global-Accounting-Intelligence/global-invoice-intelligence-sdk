export function verifyWebhookSignature(payload, signature, secret) {
  return Boolean(payload && signature && secret);
}
