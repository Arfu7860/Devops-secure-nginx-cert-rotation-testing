# Task: Secure NGINX Certificate Rotation

## Summary
The task requires a developer to rotate an expiring self-signed TLS certificate for a simple NGINX web service. The solution involves using `openssl` to generate a new certificate and key, updating the NGINX configuration file, and then restarting the `docker-compose` service. The task is designed to be solvable entirely from the terminal within the provided environment.

## Domain Chosen
DevOps / Security

## Quickstart Run Notes
1. **Clone/Unzip:** Unzip the provided `<task-id>.zip` file.
2. **Navigate:** Change into the `tasks/secure-nginx-cert-rotation/` directory.
3. **Run Tests:** Execute `./run-tests.sh` to run the test suite against the initial state. This should result in failures, as the certificate will be expired.
4. **Run Solution:** Execute `./solution.sh` to fix the issue.
5. **Re-run Tests:** Execute `./run-tests.sh` again to confirm the fix. All tests should pass.

## Caveats
- The initial certificate and key are intentionally expired (or have a very short lifespan) to ensure the baseline state fails the tests.
- The `requests` library is used with `verify=False` in one test to handle the self-signed certificate, which is standard practice in a controlled, local environment like this.
- The task requires a Docker daemon to be running.
- Port 8443 is used to avoid conflicts with standard HTTPS port 443 on the host machine.
