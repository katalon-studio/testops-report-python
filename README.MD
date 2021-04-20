# Katalon TestOps Pytest Reporters

## Usage

### Configuration

#### Environment variables

Configurations will be read from environment variables, and properties file in this order.

* `TESTOPS_SERVER_URL`

    Katalon TestOps endpoint (default: `https://testops.katalon.io`).

* `TESTOPS_API_KEY`

    Your Katalon TestOps API Key.

* `TESTOPS_PROJECT_ID`

    The Katalon TestOps project that will receive the test results.

* `TESTOPS_REPORT_FOLDER`

    The local directory where test results will be written to (default: `testops-report`).

* `TESTOPS_PROXY_SERVER_TYPE`

* `TESTOPS_PROXY_HOST`

* `TESTOPS_PROXY_PORT`

* `TESTOPS_PROXY_USERNAME`

* `TESTOPS_PROXY_PASSWORD`


#### Configuration file

Create a `testops-config.json` file in the top-level directory.

```
{
    // Default value: https://testops.katalon.io
    "basePath": "",
    "apiKey": "",
    "projectId": "",
    // Default value: testops-report
    "reportFolder": "",
    "proxy": {
        "protocol": "", // Value: http, https
        "host": "",
        "port": "",
        "auth": {
            "username": "",
            "password": ""
        }
    }
}

```

#### Install testops-pytest plugin
```
python3 -m pip install testops-report
```
#### Setup testops-pytest plugin
- Add testops-pytest listener to conftest.py file
```
pytest_plugins = ["testops_pytest.listener", ]
```
- OR follow [pytest docs](https://docs.pytest.org/en/stable/writing_plugins.html#plugin-discovery-order-at-tool-startup) for adding testops-pytest listener in the way of your choice.

## Samples

https://github.com/katalon-studio-samples/testops-pytest-sample