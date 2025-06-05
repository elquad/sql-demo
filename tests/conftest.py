import pytest
from loader.schema import Source

@pytest.fixture
def good_url_row():
    return {"url": "https://example.com/", "source_id": int(Source.OPENPHISH)}

@pytest.fixture
def bad_url_row():
    return {"url": "notaurl", "source_id": int(Source.OPENPHISH)}

@pytest.fixture
def good_ip_row():
    return {"address": "192.168.3.4", "source_id": int(Source.ALIENVAULT)}

@pytest.fixture
def bad_ip_row():
    return {"address": "256.0.300.1", "source_id": int(Source.ALIENVAULT)}

@pytest.fixture
def good_alienvault_data():
    return ["192.168.1.1#4#2#Malicious Host#KR##37.0,126.0#3\n",
            "192.168.1.2#4#2#Malicious Host#KR##37.0,126.0#3\n"]

@pytest.fixture
def good_openphish_data():
    return ["http://just-a-url.com/", "http://just-another-url.com/"]

@pytest.fixture
def good_abuse_data():
    return ['# a comment that should be skipped',
            '"3557924","2025-06-04 07:01:06","https://paste.ee/d/asdf","online","2025-06-04 07:01:06","malware_download","ascii","https://urlhaus.abuse.ch/url/","abuse_ch"',
            '"3557923","2025-06-04 06:58:06","http://127.0.0.1/400/bad.exe","online","2025-06-04 06:58:06","malware_download","exe,rat,RemcosRAT","https://urlhaus.abuse.ch/url/","abuse_ch"']