---
Installation
---
Clone repo

`pip install -r requirements.txt` install requirements

`python manage.py runserver 8000` start server 

---
REST API
---
`/api/accounts/` - CRUD endpoint for Account model
`/api/<account_name>/orders/` - endpoint for maintaining Orders 
---

WEBSOCKET
---
Go to `http://localhost:8000/` and open `developer tools` on your browser, after go to `console`

run `send_subscribe()` for subscribe to socket

run `send_unsubscribe()` for unsubscribe from socket 
