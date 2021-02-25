# ckcli

# Overview

A command-line tool for interacting with the ChainKit API, written in Python.

ChainKit facilitates the registration and later validation of the integirty of digital assets.

# Usage
```bash
    pip3 install -r requirements.txt
    ./ckcli.py --help
    ./ckcli.py [command] --help
```

## Obtain an Auth Token

In order to interact with ChainKit you must provide your username and password to get an auth token. Set the auth token in the CKTOKEN environment variable with the following command:

```bash
    export CKTOKEN=$(./ckcli.py token --username [username] --password [password] | awk '{print $2}')
```

## Register an Entity

To register a hashed entity with the server, you supply your token and a hash of your asset. (this could be a file hash or anything really)

```bash
    HASH=$(md5<<<'MySpecialText') ./ckcli.py register --token $CKTOKEN --hash $HASH
```

This will return an "Entity ID" which you can later use to...

## Verify an Entity

Provide the hash and the entity id returned during registration in order to verify the integrity of your hash:

```bash
./ckcli.py verify --token $CKTOKEN --hash $HASH --id [entity_id]

```

## Get All Registered Entities

```bash
    ./ckcli.py get --token $CKTOKEN
```
