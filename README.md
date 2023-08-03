# kg-llm-interface
Langchain-powered natural language interface to RDF knowledge-graphs.

## Installation

This repository uses poetry for package management. A Makefile rule is provided to install the dependencies:

```bash
make install
```

## Configuration

Configuration variables are loaded from the `.env` file or environment variables. A template configuration file is provided in `.env.example`.

## Quickstart

You can read and run the [example notebook](aikg/notebooks/nl_sparql.ipynb) to get a quick overview of the system.
The notebook supports using the Openai API and can run locally on a laptop.

To run the notebook in a containerized environment, run:

`make notebook`

## Server

The server can be deployed as a standalone service using the script `scripts/standalone_server.sh`. It will start a uvicorn server on port 8001, use chromaDB in client-only mode and use an RDF file as knowledge graph. This should work for small datasets.


## Pipelines

Pipelines are used to execute one-time operations for preparing data before the chat server can operate. They load their configuration from the `.env` file as well, but the variables can be overriden using yaml files (run with `--help` for more info).

### Insert triples

```mermaid
flowchart LR
    RDF[RDF file] -->|insert_triples.py| SPARQL(SPARQL endpoint)
```

Insert data from an input RDF file to a SPARQL endpoint. The input file can be in any format supported by rdflib (ttl, json-ld, rdf/xlm, ...).

Location: [insert_triples.py](aikg/flows/insert_triples.py):

SPARQL configuration can be overriden by providing a yaml file following the [aikg.config.sparql.SparqlConfig](aikg/config/sparql.py) schema:

`python insert_triples --sparql-config-path sparql.yaml`

```yaml
# sparql.yaml
endpoint: http://localhost:3030/ds/query
user: admin
password: admin
```

CLI usage: `python aikg/flows/insert_triples.py`

### Chroma build

```mermaid
flowchart LR
    SPARQL(SPARQL endpoint) -->|chroma_build.py| CHROMA(ChromaDB)
```

Build the chromaDB index from a SPARQL endpoint.

Location: [chroma_build.py](aikg/flows/chroma_build.py):

CLI usage: `python aikg/flows/chroma_build.py`

Chroma and SPARQL configurations can be overriden by providing a yaml file following the [aikg.config.chroma.ChromaConfig](aikg/config/chroma.py) or [aikg.config.sparql.SparqlConfig](aikg/config/sparql.py) schemas respectively.


## Containerized service

:warning: WIP, not functional yet

The chat server can be deployed along with the front-end, SPARQL endpoint and chromaDB server using kubernetes.

```mermaid
sequenceDiagram
    Front-end->>+Chat server: question
    Chat server->>+ChromaDB: question
    ChromaDB -->ChromaDB: embed
    ChromaDB-->>-Chat server: ontology triples
    Chat server-->Chat server: generate query
    Chat server-->>+SPARQL endpoint: query
    SPARQL endpoint-->SPARQL endpoint: run query
    SPARQL endpoint-->>-Chat server: result
    Chat server-->>-Front-end: answer
```
