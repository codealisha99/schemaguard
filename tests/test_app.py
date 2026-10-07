import json
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient
import app.main as main

PROFILE = {"name": "Alisha", "age": 30, "skills": ["Python"]}

@pytest.fixture
def client():
    # New middleware instance per test: exercise production limits without cross-test counters.
    main.app.middleware_stack = None
    with TestClient(main.app) as client:
        yield client


def post(client, raw=None, **kwargs):
    return client.post('/v1/validate', json={"raw_output": json.dumps(PROFILE) if raw is None else raw, **kwargs})


def test_health_and_frontend(client):
    assert client.get('/health').json()['status'] == 'ok'
    page = client.get('/')
    assert 'Turn messy LLM output' in page.text
    assert "script-src 'self';" in page.headers['content-security-policy']
    assert client.get('/static/app.js').status_code == 200
    assert 'https://cdn.jsdelivr.net' in client.get('/docs').headers['content-security-policy']
    assert client.get('/openapi.json').status_code == 200
    schemas = client.get('/v1/schemas').json()
    assert len(schemas['schemas']) == len(schemas['definitions']) == 3


def test_valid_and_compatibility(client):
    result = post(client).json()
    assert result['status'] == 'valid'
    assert result['success'] is True and result['fallback'] is False
    assert result['data'] == result['output'] == PROFILE
    assert result['retries'] == 0 and result['validation_errors'] == []
    assert result['repair_log'] == result['repair_steps']
    assert [s['stage'] for s in result['repair_steps']] == ['parse', 'validate']


@pytest.mark.parametrize('raw,stages', [
    ('```json\n' + json.dumps(PROFILE) + '\n```', ['fences']),
    (json.dumps(PROFILE)[:-1] + ',}', ['commas']),
    ("{'name':'Alisha','age':30,'skills':['Python']}", ['quotes']),
    ("```json\n{'name':'Alisha','age':30,'skills':['Python',],}\n```", ['fences', 'quotes', 'commas']),
])
def test_supported_repairs(client, raw, stages):
    result = post(client, raw).json()
    assert result['status'] == 'repaired' and result['output'] == PROFILE
    assert [s['stage'] for s in result['repair_steps'] if s['outcome']=='repaired'] == stages
    assert result['retries'] == len(stages)


def test_string_contents_unchanged(client):
    profile = {**PROFILE, 'name': "comma,} and { brackets <script>alert(1)</script>"}
    raw = json.dumps(profile)[:-1] + ',}'
    assert post(client, raw).json()['output'] == profile
    raw = "{'name': 'O\\'Brien', 'age':30, 'skills':['Python']}"
    assert post(client, raw).json()['output']['name'] == "O'Brien"
    raw = '{"name":"Alisha", "age":30, "skills":["it\'s fine"] ,}'
    assert post(client, raw).json()['output']['skills'] == ["it's fine"]


@pytest.mark.parametrize('raw', [
    '', 'not JSON', '{"name":"Alisha"', 'prefix ' + json.dumps(PROFILE),
    '[1,2]', 'null', 'false', '{}', '{"name":"x","name":"y","age":2,"skills":[]}',
    '{"name":"x","age":NaN,"skills":[]}', '{"name":"x","age":1e999,"skills":[]}',
    "{'name': __import__('os').system('echo bad'), 'age':2, 'skills':[]}",
    "{'name': 'unfinished, 'age':2}", "{'name':'\\x41','age':2,'skills':[]}",
])
def test_failures(client, raw):
    result = post(client, raw).json()
    assert result['status'] == 'failure' and result['output'] is None
    assert result['validation_errors']


@pytest.mark.parametrize('name,obj', [
    ('ProductListing', {'title':'Keyboard','price':89.99,'currency':'USD','in_stock':True}),
    ('SupportTicket', {'subject':'Login','description':'Expired link','priority':'high','tags':['account']}),
])
def test_other_schemas(client, name, obj):
    assert post(client, json.dumps(obj), schema_name=name).json()['output'] == obj
    assert post(client, '{}', schema_name=name).json()['status'] == 'failure'


def test_schema_types_and_paths(client):
    result = post(client, '{"name":"x","age":"30","skills":[2]}').json()
    assert result['status'] == 'failure'
    assert {e['path'] for e in result['validation_errors']} == {'age','skills.0'}
    assert result['validation_errors'][0]['expected']['type'] == 'integer'
    assert not any(s['outcome']=='repaired' for s in result['repair_steps'])
    assert post(client, json.dumps({**PROFILE,'extra':True})).json()['status']=='failure'


def test_fallback(client):
    result = post(client, 'broken', fallback=PROFILE).json()
    assert result['status']=='fallback' and result['output']==PROFILE
    assert result['fallback'] is True and result['success'] is False
    assert result['validation_errors'][0]['source']=='input'
    result = post(client, 'broken', fallback={'age':'old'}).json()
    assert result['status']=='failure' and result['output'] is None and not result['fallback']
    assert any(e['source']=='fallback' for e in result['validation_errors'])
    assert post(client, fallback={}).json()['status']=='valid'
    for schema in ('ProductListing','SupportTicket'):
        assert post(client, 'broken', schema_name=schema, fallback=PROFILE).json()['status']=='failure'


def test_request_isolation(client):
    def run(i):
        return post(client, json.dumps({**PROFILE, 'name':str(i), 'age':'private-'+str(i)})).json()
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(run, range(20)))
    assert all(len(r['repair_steps'])==2 for r in results)
    assert all('private-' not in json.dumps(r) for r in results)
    valid = post(client).json()
    assert valid['validation_errors']==[] and len(valid['repair_log'])==2


@pytest.mark.parametrize('retries', [-1,4,1000,1.5,True])
def test_retry_bounds(client, retries):
    assert post(client, max_retries=retries).status_code == 422


def test_retry_budget(client):
    raw = "```json\n{'name':'Alisha','age':30,'skills':['Python'],}\n```"
    assert post(client, raw, max_retries=0).json()['retries']==0
    assert post(client, raw, max_retries=2).json()['status']=='failure'
    assert post(client, raw, max_retries=3).json()['status']=='repaired'


def test_input_and_resource_limits(client):
    assert post(client, 'x'*16385).status_code==422
    assert 'xxxxx' not in post(client, 'x'*16385).text
    assert client.post('/v1/validate', content=b'x'*65537).status_code==413
    assert post(client, '['*33 + '0' + ']'*33).json()['status']=='failure'
    assert post(client, json.dumps([0]*4097)).json()['status']=='failure'
    assert client.post('/v1/validate', content='['*33+'0'+']'*33, headers={'content-type':'application/json'}).status_code==422
    assert client.post('/v1/validate', content=b'\xff').status_code==422
    assert post(client, 'bad', fallback={'skills':[0]*4097}).json()['status']=='failure'


def test_unknown_schema(client):
    assert post(client, schema_name='Unknown').status_code==404


def test_rate_limits(client, monkeypatch):
    monkeypatch.setattr(main, 'RATE_LIMIT', 2)
    assert post(client).status_code==200
    assert post(client).status_code==200
    result = post(client)
    assert result.status_code==429 and result.headers['retry-after']=='60'
    assert client.get('/health').status_code==200


def test_global_rate_limit(client, monkeypatch):
    monkeypatch.setattr(main, 'GLOBAL_LIMIT', 1)
    assert post(client).status_code==200
    assert post(client).status_code==429


def test_100_repairs(client, monkeypatch):
    # Regression of original 100-sample behavior, with rate limiting tested separately.
    monkeypatch.setattr(main, 'RATE_LIMIT', 120)
    for i in range(100):
        result = post(client, "{'name':'u%d','age':20,'skills':['x'],}" % i).json()
        assert result['status']=='repaired' and result['output']['name']=='u%d' % i


def test_html_content_and_errors(client):
    marker = '<img src=x onerror=alert(1)>'
    result = post(client, json.dumps({**PROFILE,'name':marker})).json()
    assert result['output']['name']==marker
    result = post(client, json.dumps({**PROFILE,'age':marker})).json()
    assert marker not in json.dumps(result)
    assert result['status']=='failure'


def test_formatting_safe_and_schema_independent(client):
    obj = {'x':'<script>', 'nested':[1, True]}
    result = client.post('/v1/format', json={'raw_output':json.dumps(obj)})
    assert result.status_code == 200 and json.loads(result.json()['formatted']) == obj
    for raw in ('{"x":1,"x":2}', '{"x":NaN}', 'broken', "{'x':1}"):
        assert client.post('/v1/format', json={'raw_output':raw}).status_code == 422
    errors = post(client, '{"name":"x","age":30,"skills":[2]}').json()['validation_errors']
    assert errors[0]['expected']['type'] == 'string'
