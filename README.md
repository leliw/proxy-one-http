# Proxy One HTTP

It's tool to capture http(s) requests and save it in local folder.

## Run docker image

```bash
docker pull ghcr.io/leliw/proxy-one-http:latest
docker run -p 8000:8000 ghcr.io/leliw/proxy-one-http:latest
```

## Run in development environment

Create a file `frontend/src/proxy.conf.json`.
Mind that `localhost` and `127.0.0.1` is not the same
in Node v. 17 (see: <https://angular.io/guide/build>).

```json
{
    "/api": {
        "target": "http://127.0.0.1:8000",
        "secure": false,
        "changeOrigin": true,
        "logLevel": "debug"
    }
}
```

Run backend in one terminal,

```bash
cd backend
uvicorn main:app --reload
```

and frontend in another terminal.

```bash
cd frontend
ng serve --proxy-config=src/proxy.conf.json
```
