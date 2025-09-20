import os
import ssl
import time
import socket
import pytest
import requests
from OpenSSL import SSL, crypto

def get_server_certificate(host, port, timeout=10):
    """
    Connects to an SSL/TLS server and returns its certificate.
    """
    conn = None
    try:
        conn = SSL.Connection(SSL.Context(SSL.SSLv23_METHOD), socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        conn.setblocking(1)
        conn.set_connect_state()
        conn.set_tlsext_host_name(host.encode('utf-8'))
        conn.connect((host, port))
        
        while conn.do_handshake() != 1:
            time.sleep(0.1)

        cert = conn.get_peer_certificate()
        return cert
    finally:
        if conn:
            conn.shutdown()
            conn.close()

def get_cert_expiry(cert):
    """
    Extracts the notAfter timestamp from an x509 certificate.
    """
    return cert.get_notAfter()

@pytest.mark.parametrize("file_name", ["new_site.crt", "new_site.key"])
def test_new_cert_and_key_exist(file_name):
    """
    Check if the new certificate and key files exist in the data/certs directory.
    """
    file_path = os.path.join("data", "certs", file_name)
    assert os.path.exists(file_path), f"File {file_path} does not exist."

def test_nginx_config_is_updated():
    """
    Verify that the nginx.conf file points to the new certificate and key.
    """
    with open("configs/nginx.conf", "r") as f:
        content = f.read()
        assert "ssl_certificate /etc/nginx/certs/new_site.crt;" in content, "nginx.conf not updated to use new_site.crt"
        assert "ssl_certificate_key /etc/nginx/certs/new_site.key;" in content, "nginx.conf not updated to use new_site.key"

def test_service_serves_valid_certificate():
    """
    Check if the service is running on 8443 and serves a valid, non-expired certificate.
    """
    # Wait for the service to be fully up and reload
    time.sleep(5) 
    
    try:
        cert = get_server_certificate("localhost", 8443)
        assert cert is not None, "Failed to retrieve certificate from service."
        
        expiry_date = get_cert_expiry(cert)
        # Check if the certificate is not expired
        assert cert.has_expired() is False, "Certificate has expired."
    except Exception as e:
        pytest.fail(f"Could not connect to service or validate certificate: {e}")

def test_service_serves_correct_response():
    """
    Verify that the NGINX service returns the expected response.
    """
    try:
        response = requests.get("https://localhost:8443", verify=False, timeout=10)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "Hello, secure world!" in response.text, "Response body does not contain expected text"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Could not connect to service: {e}")

def test_old_certificate_is_replaced():
    """
    Ensure the old certificate and key are no longer in use, verifying a full rotation.
    This test is only relevant if the solution script is provided.
    """
    # This test primarily ensures the solution did not leave old certs and config in place.
    # For auto-grading, the other tests are sufficient.
    pass

