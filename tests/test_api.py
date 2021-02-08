import pytest
import requests
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

pytest_plugins = ["docker_compose"]

# Invoking this fixture: 'function_scoped_container_getter' starts all services
@pytest.fixture(scope="function")
def wait_for_api(function_scoped_container_getter):
    """Wait for the api from my_api_service to become responsive"""
    request_session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))

    service = function_scoped_container_getter.get("webserver").network_info[0]
    api_url = "http://%s/" % (service.hostname)
    assert request_session.get(api_url)
    return request_session, api_url

def test_register(wait_for_api):
    """The Api is now verified good to go and tests can interact with it"""
    request_session, api_url = wait_for_api
    data = '{"MemberNationalAssociationId": "084001677","MemberEmail": "dconroy@gmail.com","MemberFirstName": "David","MemberLastName": "Conroy","license_data": [{"agency": "NY","number": "1234586","type": "Broker"},{"agency": "NY","number": "a12356","type": "Appraisal"},{"agency": "MA","number": "78910","type": "Salesperson"},{"agency": "NH","number": "654321","type": "Salesperson"}]}'
    item = request_session.post('%s/register' % api_url, data = data).json()
    assert item['status'] == True

def test_query(wait_for_api):
    """The Api is now verified good to go and tests can interact with it"""
    request_session, api_url = wait_for_api
    data = '{"MemberNationalAssociationId": "084001677","MemberEmail": "dconroy@gmail.com","MemberFirstName": "David","MemberLastName": "Conroy"}'
    item = request_session.post('%s/query' % api_url, data = data).json()
    assert item['status'] == True
    print("ohai")
    #request_session.delete(urljoin(api_url, 'items/2'))
