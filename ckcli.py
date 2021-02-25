#!/usr/bin/env python3

default_endpoint = "https://api.chainkit.com"
default_storage = "pencil"

try:
    import click, json, os, requests
except ImportError:
    raise
    print("Please run 'pip3 install -r requirements.txt'")
    exit(1)

@click.group()
def cli():
   pass

# Register a hash
@cli.command(name='register' , help='Register a hashed entity with the server')
@click.option('--token'      , '-t', required=True, help='Chainkit Access Token')
@click.option('--server'     , '-s', required=True, default=default_endpoint, help='The ChainKit API')
@click.option('--backend'    , '-b', required=True, default=default_storage, help='The storage backend')
@click.option('--hash'       , '-h', required=True, help='A hash of your data')
@click.option('--description', '-d', help='Description of Hash', default='Auto-Commited by Chainkit')
def register(token, server, backend, hash, description):

  description = description or 'Registered from ckcli'

  d = { "hash": hash, "storage": backend, "description": description }

  headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+token}
  r = requests.post(server+'/register', headers=headers, json=d)
  j = r.json()
  click.echo("id: "+ str(j["assetId"]))

# Verify a hash against an entity
@cli.command(name='verify', help='Verify an entity hash')
@click.option('--token'   , '-t', required=True, help='Chainkit Access Token')
@click.option('--server'  , '-s', required=True, default=default_endpoint, help='The ChainKit API')
@click.option('--backend' , '-b', required=True, default=default_storage, help='The storage backend')
@click.option('--hash'    , '-h', required=True, help='The hash of your data')
@click.option('--id'      , '-i', required=True, help='The entity id (returned during registration)')
def verify(token, server, backend, hash, id):

  headers = {'Authorization': 'Bearer '+token}
  r = requests.get(server+'/verify/'+id+'?storage='+backend+'&hash='+hash, headers=headers)
  j = r.json()

  if j.get('verified'):
    click.echo("The hash '"+hash+"' has successfully verified against the entity '"+id+"'")
    exit(0)
  else:
    click.echo("The hash '"+hash+"' has FAILED verification against the entity '"+id+"'")
    exit(1)

# Get all registered entities
@cli.command(name='get'   , help='Get all registered entities')
@click.option('--token'   , '-t', required=True, help='Chainkit Access Token')
@click.option('--server'  , '-s', required=True, default=default_endpoint, help='The ChainKit API')
def get(token, server):

  headers = {'Authorization': 'Bearer '+token}
  r = requests.get(server+'/getEntityId/', headers=headers)
  j = r.json()

  click.echo(json.dumps(j, indent=4, sort_keys=True))

# Get an API access token
@cli.command(name='token' , help='Get an API token')
@click.option('--username', '-u', required=True, help='Chainkit User Id')
@click.option('--password', '-p', required=True, help='Chainkit Password')
@click.option('--server'  , '-s', required=True, default=default_endpoint, help='The ChainKit API')
def get_token(username, password, server):
  d = {"userId": username, "password": password}
  headers = {'host': 'api.chainkit.com', 'Content-Type': 'application/json'}
  r = requests.post(server+'/token', headers=headers, json=d)
  j = r.json()
  token = j["data"]["accessToken"]

  click.echo("token: " +token)

if __name__ == '__main__':
  cli()
