# GLORY BE TO GOD

# Phone Number Validation API

**By Israel Mafabi Emmanuel**

A simple, powerful, and ready-to-deploy Flask API for validating and retrieving detailed information about any phone number worldwide. This project is built to be deployed as a microservice, for example on Google Cloud Run or via RapidAPI.

---

## ✨ Features

-   **Validation**: Checks if a phone number is valid and possible.
-   **Rich Data**: Retrieves key information including:
    -   Country Code
    -   National Number
    -   Multiple Formats (E.164, International, National)
    -   Geographic Location (e.g., "Nairobi, Kenya")
    -   Carrier Information (e.g., "Safaricom")
    -   Associated Timezones
-   **Secure**: Designed to work behind a proxy like RapidAPI, secured by a proxy secret.
-   **Production-Ready**: Comes with a `Dockerfile` for easy containerization and deployment.

---

## 🚀 API Usage

### Endpoint: `/validate`

Validates a phone number and returns its details.

-   **Method**: `GET`
-   **Headers**:
    -   `X-RapidAPI-Proxy-Secret`: **Required**. Your secret key for API access.
-   **Query Parameters**:
    -   `number`: **Required**. The phone number to validate, preferably in international format (e.g., `+254743968877`).

---

### Example Request

Here is an example using `curl`:

```bash
curl -X GET \
  -H "X-RapidAPI-Proxy-Secret: YOUR_SECRET_KEY_HERE" \
  "https://your-api-domain.com/validate?number=%2B14155552671"
```

*(Note: The `+` sign is URL-encoded as `%2B`)*

### Example Success Response (200 OK)

```json
{
  "carrier": "AT&T",
  "country_code": 1,
  "e164_format": "+14155552671",
  "input_number": "+14155552671",
  "international_format": "+1 415-555-2671",
  "is_valid": true,
  "location": "San Francisco, CA",
  "national_format": "(415) 555-2671",
  "national_number": "4155552671",
  "timezones": [
    "America/Los_Angeles"
  ]
}
```

### Example Error Response (400 Bad Request)

```json
{
  "error": "Missing required parameter: 'number'"
}
```

---

## 🔧 Running Locally

To run this project on your local machine for development:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Israel-Mafabi-Emmanuel/this-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set the environment variable for the secret:**
    ```bash
    # For Linux/macOS
    export RAPIDAPI_PROXY_SECRET="your-local-test-secret"

    # For Windows
    set RAPIDAPI_PROXY_SECRET="your-local-test-secret"
    ```

5.  **Run the Flask development server:**
    ```bash
    python api/app.py
    ```

The API will now be running at `http://127.0.0.1:5000`.
---

Made with Love 💖💖💖, <br>
**Glory be to God**