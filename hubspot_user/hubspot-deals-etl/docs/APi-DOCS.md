# Deals Service - API Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URLs](#base-urls)
4. [Common Response Formats](#common-response-formats)
5. [API Endpoints](#api-endpoints)
6. [Health & Stats Endpoints](#health--stats-endpoints)
7. [Error Handling](#error-handling)
8. [Examples](#examples)
9. [Rate Limiting](#rate-limiting)
10. [Changelog](#changelog)

## 🔍 Overview

Deals Service is a RESTful API that extracts, manages, and serves deal data from HubSpot CRM.

### API Version
- **Version**: `v1`
- **Base Path**: `/api/v1`
- **Content Type**: `application/json`
- **Documentation**: Available at `/docs` (Swagger UI)

### Key Features
- **Deal Extraction**: Fetches and paginates deal records from HubSpot CRM via the `/crm/v3/objects/deals` endpoint
- **Scan Job Management**: Tracks extraction jobs with status, progress, and error reporting via a `scans` table
- **Result Persistance**: Stores extracted deal data (name, amount, stage, pipeline, close date, etc.) in a structured `results` table
- **Association Support**: Optionally retrieves deal relationships to contacts, companies, and line items
- **Rate Limit Handling**: Respects HubSpot's API limits with retry/backoff support

## 🔐 Authentication

Deals Service authenticates with HubSpot using a **Bearer token** (Private App Access Token). Include the token in the `Authorization` header of every request along with `Content-Type: application/json`.

### Required Credentials
- **HubSpot Access Token**: Private App Access Token used as the Bearer token in the `Authorization` header
- **Content-Type**: Must be set to `application/json` on all requests

### Required Permissions
- `crm.objects.deals.read` - Fetch, search, and list deal records

### Authentication Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

## 🌐 Base URLs

### Development
```
http://localhost:8080/api/v1
```

### Staging
```
https://staging-api.your-domain.com/api/v1
```

### Production
```
https://api.your-domain.com/api/v1
```

### Swagger Documentation
```
http://localhost:8080/docs
```

## 📊 Common Response Formats

### Success Response
```json
{
  "status": "success",
  "data": {},
  "message": "Operation completed successfully",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response (Validation)
```json
{
  "status": "error",
  "message": "Input validation failed",
  "errors": {
    "[field_name]": "Field is required"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response (Application Logic)
```json
{
  "status": "error",
  "error_code": "RESOURCE_NOT_FOUND",
  "message": "The requested resource was not found",
  "details": {},
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Pagination Response
```json
{
  "pagination": {
    "current_page": 1,
    "page_size": 50,
    "total_items": 150,
    "total_pages": 3,
    "has_next": true,
    "has_previous": false,
    "next_page": 2,
    "previous_page": null
  }
}
```

## 🔍 Scan Endpoints

### 1. Start Extraction

**POST** `/scan/start`

Initiates a new deal extraction process for the specified environment.

#### Request Body
```json
{
  "config": {
    "scanId": "unique-scan-identifier",
    "type": ["deals"],
    "auth": {
      "access_token": "<hubspot_private_app_access_token>"
    }
  }
}
```

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `config.scanId` | string | Yes | Unique identifier for the scan (alphanumeric, hyphens, underscores only, max 255 chars) |
| `config.type` | array | Yes | Service types to scan (must include "deal") |
| `config.auth.access_token` | string | Yes | HubSpot Private App Access Token |
| `config.dateRange.startDate` | string | Yes | Start date (YYYY-MM-DD format) |
| `config.dateRange.endDate` | string | Yes | End date (YYYY-MM-DD format) |

#### Response
```json
{
  "success": true,
  "message": "Scan initialization accepted and is now processing in the background."
}
```

#### Status Codes
- **202**: Extraction started successfully
- **400**: Invalid request data
- **409**: Extraction already in progress/Already exists
- **500**: Internal server error

---

### 2. Get Extraction Status

**GET** `/scan/status/{scan_id}`

Retrieves the current status of an extraction process.

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scan_id` | string | Yes | Unique scan identifier |

#### Response (Existing Extraction)
```json
{
  "success": true,
  "data": {
    "scanId": "deals-scan-001",
    "organizationId": "your-org-id",
    "type": "deals",
    "status": "completed",
    "startTime": "2026-05-06T07:34:15.120585+00:00",
    "endTime": "2026-05-06T07:34:17.918669+00:00",
    "recordsExtracted": 5,
    "errorMessage": null,
    "config": {
      "filters": {
        "includeArchived": false
      },
    },
    "metadata": {
      "extraction_summary": {
        "total_records": 5
      },
    },
    "duration": 2.798084,
  }
}
```

#### Response (Non-existent Extraction)
```json
{
  "success": false,
  "message": "No scan found with ID: deals-scan-404",
  "error": "No scan found with ID: deals-scan-404"
}
```

#### Status Values
- **pending**: Extraction queued but not started
- **running**: Extraction in progress
- **completed**: Extraction finished successfully
- **failed**: Extraction failed with error
- **cancelled**: Extraction cancelled by user
- **not_found**: Extraction does not exist

#### Status Codes
- **200**: Always returns 200 (check `status` field for actual state)
- **400**: Invalid scan ID format

---

### 3. Cancel Extraction

**POST** `/scan/cancel/{scan_id}`

Cancels an ongoing extraction process.

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scan_id` | string | Yes | Unique scan identifier |

#### Response
```json
{
  "success": true,
  "scanId": "deals-scan-004",
  "status": "cancelled",
  "message": "Job cancelled successfully"
}
```

#### Status Codes
- **200**: Extraction cancelled successfully
- **400**: Invalid scan ID format or extraction cannot be cancelled
- **404**: Extraction not found
- **500**: Internal server error

---

### 4. Remove Extraction

**DELETE** `/scan/remove/{scan_id}`

Removes an extraction and all associated data from the system.

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scan_id` | string | Yes | Unique scan identifier |

#### Response
```json
{
  "success": true,
  "message": "Scan deals-scan-004 successfully removed",
  "data": {
    "scanId": "deals-scan-004",
    "tablesRemoved": 0,
    "metadataRemoved": true
  }
}
```

#### Status Codes
- **200**: Extraction removed successfully
- **400**: Invalid scan ID format or extraction cannot be removed
- **404**: Extraction not found
- **500**: Internal server error

---

### 5. Get Extraction Results

**GET** `/scan/result/{scan_id}`

Retrieves paginated extraction results with full event details.

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scan_id` | string | Yes | Unique scan identifier |

#### Query Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number (minimum: 1) |
| `page_size` | integer | No | 100 | Events per page (1-1000) |

#### Response
```json
{
  "success": true,
  "data": {
    "scanId": "deals-scan-001",
    "tableName": "hubspot_deals",
    "records": [
      {
        "id": "323237593819",
        "dealname": "TechNova - Starter Plan Upgrade",
        "amount": 5000.0,
        "closedate": "2026-06-15T05:43:37.400000+00:00",
        "dealstage": "contractsent",
        "pipeline": "default",
        "hubspot_owner_id": "91676456",
        "hs_is_closed": false,
        "hs_is_closed_won": false,
        "hs_deal_stage_probability": 0.9,
        "archived": false
      }
    ],
    "pagination": {
      "total": 5,
      "limit": 100,
      "offset": 0,
      "hasMore": false,
      "totalPages": 1
    }
  }
}
```

#### Status Codes
- **200**: Results retrieved successfully
- **400**: Invalid scan ID format or pagination parameters
- **404**: Extraction not found
- **500**: Internal server error

---

### 6. Download Extraction Results

**GET** `/scan/download/{scan_id}/{format}`

Downloads extraction results in the specified format.

#### Path Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `scan_id` | string | Yes | Unique scan identifier |
| `format` | string | Yes | Download format (json, csv, excel) |

#### Supported Formats
- **json**: JSON format with pretty printing
- **csv**: Comma-separated values with headers
- **excel**: Microsoft Excel (.xlsx) format

#### Response
File download with appropriate content-type and Content-Disposition headers:
- **JSON**: `Content-Type: application/json`
- **CSV**: `Content-Type: text/csv`
- **Excel**: `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

#### Status Codes
- **200**: File download initiated
- **400**: Invalid scan ID format or unsupported format
- **404**: Extraction not found
- **500**: Internal server error

#### Example URLs
```
GET /scan/download/my-scan-001/json
GET /scan/download/my-scan-001/csv
GET /scan/download/my-scan-001/excel
```

---

## 🏥 Health & Stats Endpoints

### 1. Health Check

**GET** `/health`

Returns the overall health status of the service.

#### Response (Healthy)
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "service": "[Service Name]",
  "version": "1.0.0",
  "checks": {
    "database": "healthy",
    "cache": "healthy",
    "external_api": "healthy"
  }
}
```

#### Response (Unhealthy)
```json
{
  "status": "unhealthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "service": "[Service Name]",
  "version": "1.0.0",
  "checks": {
    "database": "unhealthy: connection timeout",
    "cache": "healthy",
    "external_api": "degraded: high latency"
  }
}
```

#### Status Codes
- **200**: Service is healthy
- **503**: Service is unhealthy

---

### 2. Service Statistics

**GET** `/stats`

Returns comprehensive service statistics and performance metrics.

#### Response
```json
{
  "total_requests": 15000,
  "active_connections": 23,
  "success_rate": 99.5,
  "average_response_time": 125.5,
  "errors_last_hour": 5,
  "uptime": "7 days, 3:24:15",
  "memory_usage": "512MB",
  "cpu_usage": "15%",
  "last_restart": "2024-01-08T10:30:00Z"
}
```

#### Status Codes
- **200**: Statistics retrieved successfully
- **500**: Internal server error

---

## ⚠️ Error Handling

### Error Response Formats

#### Validation Errors (400)
Returned for input validation failures:
```json
{
  "status": "error",
  "error_code": "VALIDATION_ERROR",
  "message": "Input validation failed",
  "errors": {
    "[field_name]": "[error_message]"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Authentication Errors (401)
```json
{
  "status": "error",
  "error_code": "UNAUTHORIZED",
  "message": "Authentication required",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Authorization Errors (403)
```json
{
  "status": "error",
  "error_code": "FORBIDDEN",
  "message": "Insufficient permissions",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Not Found Errors (404)
```json
{
  "status": "error",
  "error_code": "NOT_FOUND",
  "message": "Resource not found",
  "resource_id": "[id]",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Conflict Errors (409)
```json
{
  "status": "error",
  "error_code": "CONFLICT",
  "message": "Resource already exists",
  "conflicting_field": "[field_name]",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Rate Limit Errors (429)
```json
{
  "status": "error",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests",
  "retry_after": 60,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Server Errors (500)
```json
{
  "status": "error",
  "error_code": "INTERNAL_ERROR",
  "message": "An unexpected error occurred",
  "incident_id": "inc_123456",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

| Code                        | Description                     |
|-----------------------------|---------------------------------|
| `VALIDATION_ERROR`          | Input validation failed         |
| `UNAUTHORIZED`              | Authentication required         |
| `FORBIDDEN`                 | Insufficient permissions        |
| `NOT_FOUND`                 | Resource not found              |
| `CONFLICT`                  | Resource already exists         |
| `RATE_LIMIT_EXCEEDED`       | Too many requests               |
| `INTERNAL_ERROR`            | Server error                    |
| `SERVICE_UNAVAILABLE`       | Service temporarily unavailable |

---

## 📚 Examples

### Complete Extraction Workflow

#### 1. Start Extraction
```bash
curl -X POST "https://api.your-domain.com/scan/start" \
  -H "Content-Type: application/json" \
  -d '{
    "config": {
      "scanId": "deals-sync-001",
      "type": ["deals"],
      "auth": {
        "access_token": "pat-na1-..."
      }
    }
  }'
```

#### 2. Monitor Progress
```bash
curl "https://api.your-domain.com/scan/status/deals-sync-001"
```

#### 3. Get Results
```bash
curl "https://api.your-domain.com/scan/result/deals-sync-001?page=1&page_size=50"
```

#### 4. Download Results
```bash
# Download as CSV
curl "https://api.your-domain.com/scan/download/deals-sync-001/csv" \
  -o "deals_results.csv"

# Download as Excel
curl "https://api.your-domain.com/scan/download/deals-sync-001/excel" \
  -o "deals_results.xlsx"

# Download as JSON
curl "https://api.your-domain.com/scan/download/deals-sync-001/json" \
  -o "deals_results.json"
```

#### 5. Cancel Extraction (if needed)
```bash
curl -X POST "https://api.your-domain.com/scan/cancel/deals-sync-001"
```

#### 6. Remove Extraction (cleanup)
```bash
curl -X DELETE "https://api.your-domain.com/scan/remove/deals-sync-001"
```

### PowerShell Examples

#### Start Extraction
```powershell
$body = @{
  config = @{
    scanId = "deals-sync-001"
    type = @("deals")
    auth = @{
      access_token = "pat-na1-..."
    }
  }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "https://api.your-domain.com/scan/start" -Method Post -Body $body -ContentType "application/json"
```

#### Get Status
```powershell
Invoke-RestMethod -Uri "https://api.your-domain.com/scan/status/deals-sync-001"
```

#### Download Results
```powershell
# Download Excel file
Invoke-WebRequest -Uri "https://api.your-domain.com/scan/download/deals-sync-001/excel" -OutFile "results.xlsx"

# Download CSV file
Invoke-WebRequest -Uri "https://api.your-domain.com/scan/download/deals-sync-001/csv" -OutFile "results.csv"
```

### Python Examples

#### Start Extraction
```python
import requests

url = "https://api.your-domain.com/scan/start"
payload = {
    "config": {
        "scanId": "deals-sync-001",
        "type": ["deals"],
        "auth": {
            "access_token": "pat-na..."
        }
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

#### Monitor Progress
```python
import requests
import time

scan_id = "deals-sync-001"
url = f"https://api.your-domain.com/scan/status/{scan_id}"

while True:
    response = requests.get(url)
    status = response.json()

    print(f"Status: {status['status']}")
    if status.get("progress"):
        p = status["progress"]
        print(f"  Extracted: {p['deals_extracted']} / {p['total_deals']} ({p['failed_deals']} failed)")

    if status["status"] in ["completed", "failed", "cancelled", "not_found"]:
        break

    time.sleep(10)  # Check every 10 seconds
```

#### Get Paginated Results
```python
import requests

scan_id = "deals-sync-001"
page = 1
all_deals = []

while True:
    url = f"https://api.your-domain.com/scan/result/{scan_id}?page={page}&page_size=100"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        all_deals.extend(data["data"])

        if not data["pagination"]["has_next"]:
            break

        page += 1
    else:
        print(f"Error: {response.status_code}")
        break

print(f"Total deals retrieved: {len(all_deals)}")
```

#### Download Results
```python
import requests

scan_id = "deals-sync-001"

formats = ["json", "csv", "excel"]
for fmt in formats:
    url = f"https://api.your-domain.com/scan/download/{scan_id}/{fmt}"
    response = requests.get(url)

    if response.status_code == 200:
        filename = f"deals_results.{fmt if fmt != 'excel' else 'xlsx'}"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {fmt}: {response.status_code}")
```

#### Error Handling
```python
import requests