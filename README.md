# CSV to SQLite with ChatGPT Integration
by Joshua Arrevillaga

<p>
This project implements a command line tool to load in files into a SQLite database, it creates tables dynamically, executes SQL queries, and generate queries using ChatGPT 3.5 turbo by using OpenAI's API 
</p>

## Requirements
Podman: 
```bash
brew install podman
```

## Running
``` bash
podman build -t google-sheets-clone .

podman run --rm -it google-sheets-clone

```
