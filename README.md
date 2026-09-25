# SlotSentry

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=flat-square&logo=flask&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat-square&logo=uv&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-2ea44f?style=flat-square)

SlotSentry is a simple REST API for creating and managing appointment-watch requests.

The project is built with Flask and currently stores all data **in memory**, without using a database.

## Features

* Create a new appointment-watch request
* Get a single watch
* Get all watches
* Partially update a watch
* Delete a watch
* RESTful API design
* In-memory data storage
* API testing with Postman
* Code linting with Ruff

---

## API Endpoints

### 1. Create a Watch

**POST** `/watches`

Creates a new watch request.

#### Request Body

```json
{
  "title": "نوبت سفارت آلمان",
  "check_interval_minutes": 15,
  "contact_email": "test@example.com"
}
```

#### Response

**201 Created**

```json
{
  "id": 1,
  "status": "active",
  "title": "نوبت سفارت آلمان",
  "check_interval_minutes": 15,
  "contact_email": "test@example.com"
}
```

If a required field is missing:

**400 Bad Request**

```json
{
  "response": "Missing required field: title"
}
```

---

### 2. Get a Watch

**GET** `/watches/<id>`

Returns a specific watch by its ID.

#### Example

`GET /watches/1`

#### Response

**200 OK**

```json
{
  "id": 1,
  "status": "active",
  "title": "نوبت سفارت آلمان",
  "check_interval_minutes": 15,
  "contact_email": "test@example.com"
}
```

If the watch does not exist:

**404 Not Found**

```json
{
  "response": "Watch does not exist"
}
```

---

### 3. Get All Watches

**GET** `/watches`

Returns all watch requests.

#### Response

**200 OK**

```json
[
  {
    "id": 1,
    "status": "active",
    "title": "نوبت سفارت آلمان",
    "check_interval_minutes": 15,
    "contact_email": "test@example.com"
  },
  {
    "id": 2,
    "status": "active",
    "title": "نوبت سفارت فرانسه",
    "check_interval_minutes": 30,
    "contact_email": "test@example.com"
  }
]
```

---

### 4. Update a Watch

**PATCH** `/watches/<id>`

Updates one or more fields of an existing watch.

The watch ID is provided in the URL, not in the request body.

#### Request Body

For example, to pause a watch:

```json
{
  "status": "paused"
}
```

Or to change the check interval:

```json
{
  "check_interval_minutes": 30
}
```

#### Response

**200 OK**

Returns the updated watch.

If the watch does not exist:

**404 Not Found**

```json
{
  "response": "Watch does not exist"
}
```

---

### 5. Delete a Watch

**DELETE** `/watches/<id>`

Deletes an existing watch.

#### Response

**204 No Content**

No response body is returned when the deletion is successful.

If the watch does not exist:

**404 Not Found**

```json
{
  "response": "Watch does not exist"
}
```

---

## HTTP Status Codes

| Status Code | Meaning                    |
| ----------- | -------------------------- |
| `200`       | Request successful         |
| `201`       | Watch successfully created |
| `204`       | Watch successfully deleted |
| `400`       | Invalid request            |
| `404`       | Watch not found            |

---

## Data Storage

The project currently uses an **in-memory Python data structure** to store watches.

No database is required at this stage.

Because the data is stored in memory, all watches are lost when the application stops or restarts.

---

## Testing

The APIs were tested using **Postman**.

The main scenarios tested include:

* Creating watches
* Getting individual watches
* Getting all watches
* Updating watch fields
* Pausing a watch
* Deleting watches
* Handling missing watches with `404`
* Handling invalid requests with `400`

---

## Code Quality

The project uses **Ruff** for Python linting.

Run the following command to check the project:

```bash
ruff check .
```

A successful check should return:

```text
All checks passed!
```

---

## Running the Application

Install the project dependencies and run the Flask application.

The application is configured to run on:

```text
http://localhost:8000
```

---

## Project Roadmap

The project is planned to grow in several stages:

* [x] RESTful API
* [x] In-memory data storage
* [x] Postman testing
* [x] Ruff linting
* [ ] API documentation improvements
* [ ] Dockerfile
* [ ] Docker Compose
* [ ] Docker Hub image
* [ ] Automated tests with pytest
* [ ] GitHub Actions CI/CD
* [ ] Linux server deployment
* [ ] Domain and Cloudflare configuration
* [ ] Telegram bot integration

---

## Future Architecture

The current project contains the core REST API.

In future stages, additional services such as a Telegram bot or background worker can be added alongside the API using Docker Compose.

The goal is to gradually turn SlotSentry into a small appointment-monitoring system.
