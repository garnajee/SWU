#!/usr/bin/env python3

import hashlib
import hmac

from utils.exceptions import SignatureException
from utils.logger import get_logger


def verify_signature(payload_body: str, gh_webhook_secret: str, signature_header: str):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (GITHUB_WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """

    if not signature_header:
        get_logger().error("X-Hub-Signature-256 header is missing!")
        raise SignatureException("X-Hub-Signature-256 header is missing!")

    hash_object = hmac.new(
        gh_webhook_secret.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256
    )

    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        get_logger().error("Request signatures didn't match!")
        get_logger().debug(f"EXPECTED {expected_signature}")
        get_logger().debug(f"FOUND {signature_header}")
        raise SignatureException("Request signatures didn't match!")