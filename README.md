

# Cyber Threats API Documentation

The Cyber Threats API provides endpoints to fetch, filter, and add cyber threat resources from a MongoDB database.

## Base URL

```
http://75.193.104.120:5000
```

## Endpoints

### 1. Fetch Cyber Threats by Type

- **URL**: `/cyberthreats/type`
- **Method**: `GET`
- **Parameters**:
  - `type`: (string, required) The type of cyber threat to filter by.
  
#### Example

```bash
curl -X GET "http://75.193.104.120:5000/cyberthreats/type?type=phishing"
```

### 2. Fetch Cyber Threats by Severity

- **URL**: `/cyberthreats/severity`
- **Method**: `GET`
- **Parameters**:
  - `severity`: (string, required) The severity level of cyber threat to filter by (`low`, `medium`, `high`).
  
#### Example

```bash
curl -X GET "http://75.193.104.120:5000/cyberthreats/severity?severity=high"
```

### 3. Fetch All Cyber Threats

- **URL**: `/cyberthreats`
- **Method**: `GET`

#### Example

```bash
curl -X GET "http://75.193.104.120:5000/cyberthreats"
```

### 4. Fetch a Specific Cyber Threat by ID

- **URL**: `/cyberthreats/<threat_id>`
- **Method**: `GET`
- **Path Parameters**:
  - `threat_id`: (string, required) The ID of the cyber threat to fetch.
  
#### Example

```bash
curl -X GET "http://75.193.104.120:5000/cyberthreats/1234567890abcdef"
```

### 5. Add a New Cyber Threat

- **URL**: `/cyberthreats/add`
- **Method**: `POST`
- **Request Body**:
  - `type`: (string, required) The type of cyber threat.
  - `severity`: (string, required) The severity level of the cyber threat (`low`, `medium`, `high`).
  - `description`: (string, required) Description of the cyber threat.
  
#### Example

```bash
curl -X POST -H "Content-Type: application/json" -d '{"type": "malware", "severity": "high", "description": "New malware threat"}' "http://75.193.104.120:5000/cyberthreats/add"
```
