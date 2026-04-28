# 📋 Deals API Service - Integration with HubSpot API

This document explains the HubSpot REST API endpoints required by the Deals API Service to extract DEAL data from HubSpot instances.

---

## 📋 Overview

The Deals API Service integrates with HubSpot REST API endpoints to extract DEAL information. Below are the required and optional endpoints:

### ✅ **Required Endpoint (Essential)**
| **API Endpoint**                    | **Purpose**                          | **Version** | **Required Permissions** | **Usage**    |
|-------------------------------------|--------------------------------------|-------------|--------------------------|--------------|
| `/crm/v3/objects/deals/search`    | Search and list deals           | `v3` | `crm.objects.deals.read`      | **Required** |

### 🔧 **Optional Endpoints (Advanced Features)**
| **API Endpoint**                    | **Purpose**                          | **Version** | **Required Permissions** | **Usage**    |
|-------------------------------------|--------------------------------------|-------------|--------------------------|--------------|
| `/crm/v3/objects/deals/{dealId}`         | Get detailed deal information   | `v3` | `crm.objects.deals.read`      | Optional     |
| `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}`         | Get deal associations (contacts, companies, etc.)         | `v3` | `crm.objects.deals.read`      | Optional     |
| `/crm/v3/objects/deals/{dealId}?properties`         | Get deal with specific properties       | `v3` | `crm.objects.deals.read`      | Optional     |
| `/crm/v3/objects/deals/{dealId}/associations/line_items`         | Get line items associated with deal      | `v3` | `crm.objects.deals.read`      | Optional     |

### 🎯 **Recommendation**
**Start with only the required endpoint.** The `/crm/v3/objects/deals` endpoint provides all essential deal data needed for basic DEAL analytics and extraction.

---

## 🔐 Authentication Requirements

### **Bearer Token Authentication**
```http
Authorization: HubSpot_Sample_AccessToken
Content-Type: application/json
```

### **Required Permissions**
- **`crm.objects.deals.read`**: fetch, search, & list
- **`crm.objects.deals.write`**: create, update, & delete

---

## 🌐 HubSpot API Endpoints

### 🎯 **PRIMARY ENDPOINT (Required for Basic deal Extraction)**

### 1. **Search Deals** - `/crm/v3/objects/deals` ✅ **REQUIRED**

**Purpose**: Get paginated list of all deals - **THIS IS ALL YOU NEED FOR BASIC deal EXTRACTION**

**Method**: `GET`

**URL**: `https://api.hubapi.com/crm/v3/objects/deals`

**Query Parameters**:
```
?limit=5&properties=amount&archived=false
```

**Request Example**:
```http
GET https://api.hubapi.com/crm/v3/objects/deals?limit=50&archived=false&properties=dealname,amount,closedate,dealstage
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Response Structure** (Contains ALL essential deal data):
```json
{
  "results": [
    {
      "archived": false,
      "createdAt": "2024-01-15T08:00:00Z",
      "id": "123456789",
      "properties": {
        "dealname": "Acme Corp Enterprise Deal",
        "amount": "15000.00",
        "closedate": "2024-06-30T00:00:00Z",
        "dealstage": "contractsent",
        "pipeline": "default"
      },
      "updatedAt": "2024-03-10T12:45:00Z",
      "archivedAt": null,
      "associations": {
        "contacts": { "results": [{ "id": "55001", "type": "deal_to_contact" }] },
        "companies": { "results": [{ "id": "78901", "type": "deal_to_company" }] }
      },
      "propertiesWithHistory": {},
      "url": "https://api.hubapi.com/crm/v3/objects/deals/123456789"
    }
  ],
  "paging": {
    "next": {
      "after": "NTI1Cg%3D%3D",
      "link": "?after=NTI1Cg%3D%3D"
    }
  }
}
```

**✅ This endpoint provides ALL the default deal fields:**
- `id`, `createdAt`, `updatedAt`
- `archivedAt`, `archived`, `url`
- `properties` with `dealname`, `amount`, `closedate`, `dealstage`, `pipeline`
- `associations` with linked `contacts` and `companies`
- `propertiesWithHistory` for previous field values

**Rate Limit**: 100 requests per 10 seconds, 190 requests per 10 seconds (private app)

---

## 🔧 **OPTIONAL ENDPOINTS (Advanced Features Only)**

> **⚠️ Note**: These endpoints are NOT required for basic deal extraction. Only implement if you need advanced deal analytics like pipeline stage tracking, association mapping, or property history analysis.

### 2. **Get deal details** - `/crm/v3/objects/deals/{dealId}` 🔧 **OPTIONAL**

**Purpose**: Get detailed information for a specific deal

**When to use**: Only if you need additional deal metadata not available in search

**Method**: `GET`

**URL**: `https://api.hubapi.com/crm/v3/objects/deals/{dealId}`

**Request Example**:
```http
GET https://api.hubapi.com/crm/v3/objects/deals/123456789
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Response Structure**:
```json
{
  "id": "123456789",
  "url": "https://api.hubapi.com/crm/v3/objects/deals/123456789",
  "name": "Acme Corp Enterprise Deal",
  "type": "deal",
  "propertiesWithHistory": {
    "dealstage": [
      {
        "value": "contractsent",
        "timestamp": "2024-03-01T00:00:00Z",
        "sourceType": "CRM_UI"
      }
    ],
    "amount": [
      {
        "value": "15000.00",
        "timestamp": "2024-01-15T00:00:00Z",
        "sourceType": "API"
      }
    ]
  },
  "properties": {
    "dealname": "Acme Corp Enterprise Deal",
    "amount": "15000.00",
    "closedate": "2024-06-30T00:00:00Z",
    "dealstage": "contractsent",
    "pipeline": "default"
  },
  "archived": false,
  "archivedAt": null,
  "createdAt": "2024-01-15T08:00:00Z"
}
```

---

### 3. **Get deal associations** - `/crm/v3/objects/deals/{dealId}/associations/{toObjectType}` 🔧 **OPTIONAL**

**Purpose**: Get contacts, companies, or other objects associated with a deal

**When to use**: Only if you need association mapping and relationship analysis

**Method**: `GET`

**URL**: `https://api.hubapi.com/crm/v3/objects/deals/{dealId}/associations/{toObjectType}`

**Query Parameters**:
```
?limit=50&after=NTI1Cg%3D%3D
```

**Request Example**:
```http
GET https://api.hubapi.com/crm/v3/objects/deals/123456789/associations/contacts?limit=50
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Response Structure**:
```json
{
  "results": [
    {
      "id": "55001",
      "type": "deal_to_contact"
    },
    {
      "id": "55002",
      "type": "deal_to_contact"
    }
  ],
  "paging": {
    "next": {
      "after": "NTI1Cg%3D%3D",
      "link": "?after=NTI1Cg%3D%3D"
    }
  }
}
```

---

### 4. **Get deal Configuration** - `/crm/v3/objects/deals/{dealId}?properties` 🔧 **OPTIONAL**

**Purpose**: Get deal configuration details (`dealname`, `amount`, `closedate`, etc.)

**When to use**: Only if you need to limit the response payload to specific fields

**Method**: `GET`

**URL**: `https://api.hubapi.com/crm/v3/objects/deals/{dealId}?properties=dealname,amount,closedate,dealstage,pipeline`

**Request Example**:
```http
GET https://api.hubapi.com/crm/v3/objects/deals/123456789?properties=dealname,amount,closedate,dealstage,pipeline
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Response Structure**:
```json
{
  "id": "123456789",
  "properties": {
    "dealname": "Acme Corp Enterprise Deal",
    "amount": "15000.00",
    "closedate": "2024-06-30T00:00:00Z",
    "dealstage": "contractsent",
    "pipeline": "default"
  },
  "createdAt": "2024-01-15T08:00:00Z",
  "updatedAt": "2024-03-10T12:45:00Z",
  "archived": false,
  "archivedAt": null
}
```

---

### 5. **Get deal line items** - `/crm/v3/objects/deals/{dealId}/associations/line_items` 🔧 **OPTIONAL**

**Purpose**: Get line items associated with a deal

**When to use**: Only if you need line item analysis and product-level reporting

**Method**: `GET`

**URL**: `https://api.hubapi.com/crm/v3/objects/deals/{dealId}/associations/line_items`

**Query Parameters**:
```
?limit=50&after=NTI1Cg%3D%3D&properties=name,price,quantity,amount,hs_sku&archived=false
```

**Request Example**:
```http
GET https://api.hubapi.com/crm/v3/objects/deals/123456789?associations=line_item&limit=50
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Response Structure**:
```json
{
  "results": [
    {
      "archived": false,
      "createdAt": "2024-01-15T08:00:00Z",
      "id": "LI-001",
      "properties": {
        "name": "Enterprise License",
        "price": "3000.00",
        "quantity": "5",
        "amount": "15000.00",
        "hs_sku": "ENT-LIC-001"
      },
      "updatedAt": "2024-03-10T12:45:00Z",
      "archivedAt": null,
      "associations": {
        "deals": { "results": [{ "id": "123456789", "type": "line_item_to_deal" }] }
      },
      "objectWriteTraceId": "xyz789trace",
      "propertiesWithHistory": {},
      "url": "https://api.hubapi.com/crm/v3/objects/line_items/LI-001"
    }
  ],
  "paging": {
    "next": {
      "after": "NTI1Cg%3D%3D",
      "link": "?after=NTI1Cg%3D%3D"
    }
  }
}
```

---

## 📊 Data Extraction Flow

### 🎯 **SIMPLE FLOW (Recommended - Using Only Required Endpoint)**

### **Single Endpoint Approach - `/crm/v3/objects/deals` Only**
```python
def extract_all_deals_simple():
    """Extract all deals using only the /crm/v3/objects/deals endpoint"""
    after = None
    batch_size = 50
    all_deals = []

    while True:
        params = {
            "limit": batch_size,
            "archived": False,
            "properties": "dealname,amount,closedate,dealstage,pipeline"
        }
        if after:
            params["after"] = after

        response = requests.get(
            f"{base_url}/crm/v3/objects/deals",
            params=params,
            headers=auth_headers
        )

        data = response.json()
        deals = data.get("results", [])

        if not deals:  # No more deals
            break

        all_deals.extend(deals)

        # Check if there is a next page
        after = data.get("paging", {}).get("next", {}).get("after")
        if not after:
            break

    return all_deals

# This gives you ALL essential deal data:
# - id, createdAt, updatedAt, archivedAt, archived
# - properties with dealname, amount, closedate, dealstage, pipeline
# - url for reference
```

---

### 🔧 **ADVANCED FLOW (Optional - Multiple Endpoints)**

> **⚠️ Only use this if you need detailed deal info, associations, specific properties, or line item data**

### **Step 1: Batch deal Retrieval**
```python
# Get deals in batches of 50
after = None

while True:
    response = requests.get(
        f"{base_url}/crm/v3/objects/deals",
        params={
            "limit": 50,
            "archived": False,
            "after": after
        },
        headers=auth_headers
    )
    deals_data = response.json()
    deals = deals_data.get("results", [])

    after = deals_data.get("paging", {}).get("next", {}).get("after")
    if not after:
        break
```

### **Step 2: Enhanced deal Details (Optional)**
```python
# Get detailed information for each deal
for deal in deals:
    response = requests.get(
        f"{base_url}/crm/v3/objects/deals/{deal['id']}",
        headers=auth_headers
    )
    detailed_deal = response.json()
```

### **Step 3: deal [Related Data] (Optional)**
```python
# Get associations for each deal (contacts, companies, etc.)
for deal in deals:
    for object_type in ["contacts", "companies"]:
        response = requests.get(
            f"{base_url}/crm/v3/objects/deals/{deal['id']}/associations/{object_type}",
            params={"limit": 50},
            headers=auth_headers
        )
        deal_associations = response.json()
```

### **Step 4: deal Configuration (Optional)**
```python
# Get deal with specific properties only
for deal in deals:
    response = requests.get(
        f"{base_url}/crm/v3/objects/deals/{deal['id']}",
        params={
            "properties": "dealname,amount,closedate,dealstage,pipeline"
        },
        headers=auth_headers
    )
    deal_properties = response.json()
```

---

## ⚡ Performance Considerations

### **Rate Limiting**
- **Default Limit**: [X] requests per [time period] per API token
- **Burst Limit**: [Y] requests per [time period] (short duration)
- **Best Practice**: Implement exponential backoff on [rate limit response code] responses

### **Batch Processing**
- **Recommended Batch Size**: [X] [objects] per request
- **Concurrent Requests**: Max [N] parallel requests ([objects] are complex objects)
- **Request Interval**: [X]ms between requests to stay under rate limits

### **Error Handling**
```http
# Rate limit exceeded
HTTP/[rate_limit_code] [Rate Limit Message]
Retry-After: [retry_seconds]

# Authentication failed  
HTTP/401 Unauthorized

# Insufficient permissions
HTTP/403 Forbidden

# deal not found
HTTP/404 Not Found
```

---

## 🔒 Security Requirements

### **API Token Permissions**

#### ✅ **Required (Minimum Permissions)**
```
Required Scopes:
- [scope_1] (for basic deal information)
```

#### 🔧 **Optional (Advanced Features)**
```
Additional Scopes (only if using optional endpoints):
- [scope_2] (for [related data] information)
- [scope_3] (for deal configuration)
```

### **User Permissions**

#### ✅ **Required (Minimum)**
The API token user must have:
- **[Permission_1]** global permission
- **[Permission_2]** permission

#### 🔧 **Optional (Advanced Features)**
Additional permissions (only if using optional endpoints):
- **[Permission_3]** permission (for deal configuration details)
- **[Permission_4]** (for [additional data] access)

---

## 📈 Monitoring & Debugging

### **Request Headers for Debugging**
```http
[AUTH_HEADER]: [AUTH_VALUE]
Content-Type: application/json
User-Agent: [ServiceName]/1.0
X-Request-ID: deal-scan-001-batch-1
```

### **Response Validation**
```python
def validate_object_response(object_data):
    required_fields = ["[field_id]", "[field_name]", "[field_type]", "[nested_object]"]
    for field in required_fields:
        if field not in object_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate deal type
    if object_data["[field_type]"] not in ["[type_1]", "[type_2]"]:
        raise ValueError(f"Invalid deal type: {object_data['[field_type]']}")
```

### **API Usage Metrics**
- Track requests per [time period]
- Monitor response times
- Log rate limit headers
- Track authentication failures

---

## 🧪 Testing API Integration

### **Test Authentication**
```bash
curl -X GET \
  "https://[your_instance].[platform_domain]/[api_path]/[auth_test_endpoint]" \
  -H "[AUTH_HEADER]: [AUTH_VALUE]" \
  -H "Content-Type: application/json"
```

### **Test deal Search**
```bash
curl -X GET \
  "https://[your_instance].[platform_domain]/[api_path]/[primary_endpoint]?[size_param]=5" \
  -H "[AUTH_HEADER]: [AUTH_VALUE]" \
  -H "Content-Type: application/json"
```

### **Test deal Details**
```bash
curl -X GET \
  "https://[your_instance].[platform_domain]/[api_path]/[endpoint_1]/{objectId}" \
  -H "[AUTH_HEADER]: [AUTH_VALUE]" \
  -H "Content-Type: application/json"
```

---

## 🚨 Common Issues & Solutions

### **Issue**: 401 Unauthorized
**Solution**: Verify [auth method] and [credential] combination
```bash
[verification_command]
```

### **Issue**: 403 Forbidden
**Solution**: Check user has "[Permission_1]" and "[Permission_2]" permissions

### **Issue**: [Rate Limit Code] Rate Limited
**Solution**: Implement retry with exponential backoff
```python
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

### **Issue**: Empty deal List
**Solution**: Check if user has access to [parent objects] with DEAL [objects]

### **Issue**: Need [Related Data]/Configuration But Want to Keep It Simple**
**Solution**: Start with `/[primary_endpoint]` only. Add optional endpoints later if needed for advanced DEAL analytics

---

## 💡 **Implementation Recommendations**

### 🎯 **Phase 1: Start Simple (Recommended)**
1. Implement only `/[api_path]/[primary_endpoint]`
2. Extract basic deal data ([field_id], [field_name], [field_type], [nested_object] info)
3. This covers 90% of DEAL analytics needs

### 🔧 **Phase 2: Add Advanced Features (If Needed)**
1. Add `/[api_path]/[endpoint_1]/{objectId}` for detailed deal info
2. Add `/[api_path]/[endpoint_2]/{objectId}/[related_endpoint]` for [related data] analysis  
3. Add `/[api_path]/[endpoint_3]/{objectId}/[config_endpoint]` for [workflow type] analysis
4. Add `/[api_path]/[endpoint_4]/{objectId}/[additional_endpoint]` for [additional functionality]

### ⚡ **Performance Tip**
- **Simple approach**: 1 API call per [batch_size] [objects]
- **Advanced approach**: 1 + N API calls (N = number of [objects] for details)
- Start simple to minimize API usage and complexity!

---

## 📞 Support Resources

- **HubSpot API Documentation**: [API_DOCS_URL]
- **Rate Limiting Guide**: [RATE_LIMIT_DOCS_URL]
- **Authentication Guide**: [AUTH_DOCS_URL]
- **DEAL Permissions Reference**: [PERMISSIONS_DOCS_URL]