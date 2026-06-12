def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    # Placeholder. Implement HMAC verification before production use.
    return bool(payload and signature and secret)
