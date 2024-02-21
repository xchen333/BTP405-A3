# Notes API

Created for Activity 3 in BTP405

## Setup

- Build the container:
  `sudo docker-compose build`
- Start the container:
  `sudo docker-compose up -d`

## Usage

### GET:

**Endpoint:** `/notes` – get all notes

**Response (example):**

`[
{
"id": 1,
"title": "Note 1",
"content": "Note 1 content"
},
{
"id": 2,
"title": "Note 2",
"content": "Note 2 content"
}
]`

**Endpoint:** `/note?id=<id>` – gets a specific note my id

**Response (example):**

`{
"id": 1,
"title": "Note 1",
"content": "Note 1 content"
}`

### POST:

**Endpoint:** `/`

**Body:** `{“title”: <your title>, “content”: your content}`

**Response:** `{"message": "Note added successfully"}`

### PUT:

**Endpoint:** `/notes`

**Body:** `{"id": <id>, "title": <new title>,"content": <new content>}`

**Response:** `{"message": "Note updated successfully"}`

### DELETE:

**Endpoint:** `/note?id=<id>`

**Response:** `{"message": "Note deleted successfully"}`
