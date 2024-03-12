from src.db import storage
from test.init import client, db_session, researcher_auth_headers

def test_create_coefficient_setup():
    response = client.post('/coefficient_setups/', json={"id": None, "user_id": None, "alpha": 1, "beta": 1.2, "mu": 0.3, "g": 0.4, "a": 3, "n": 5}, headers=researcher_auth_headers)
    assert response.status_code == 200

    cs = storage.get_coefficient_setup_by_id(db_session, 1)
    assert cs is not None
    assert cs.id == 1
    assert cs.user_id == 2
    assert cs.alpha == 1
    assert cs.beta == 1.2
    assert cs.mu == 0.3
    assert cs.g == 0.4
    assert cs.a == 3
    assert cs.n == 5

def test_get_coefficient_setup_by_id():
    response = client.get('/coefficient_setups/1/', headers=researcher_auth_headers)
    assert response.status_code == 200

    cs = response.json()

    assert cs is not None
    assert cs['id'] == 1
    assert cs['user_id'] == 2
    assert cs['alpha'] == 1
    assert cs['beta'] == 1.2
    assert cs['mu'] == 0.3
    assert cs['g'] == 0.4
    assert cs['a'] == 3
    assert cs['n'] == 5

def test_get_coefficient_setup_by_id_not_found():
    response = client.get('/coefficient_setups/2', headers=researcher_auth_headers)
    assert response.status_code == 404

def test_get_coefficient_setup_list():
    response = client.get('/coefficient_setups/', headers=researcher_auth_headers)
    assert response.status_code == 200

    cs_list = response.json()

    assert cs_list is not None
    assert len(cs_list['items']) == 1
    assert cs_list['total'] == 1
    assert cs_list['page'] == 1
    assert cs_list['page_size'] == 10

def test_calculate_coefficient_setup():
    response = client.post('/coefficient_setups/1/calculate/', headers=researcher_auth_headers)
    assert response.status_code == 200

    cr = response.json()
    assert cr is not None
    assert cr['id'] == 1
    assert cr['user_id'] == 2
    assert cr['alpha'] == 1
    assert cr['beta'] == 1.2
    assert cr['mu'] == 0.3
    assert cr['g'] == 0.4
    assert cr['a'] == 3
    assert cr['n'] == 5
    assert cr['t1'] == 1
    assert cr['t2'] == 1
    assert cr['s'] == 1
    assert cr['calculated_at'] is not None

def test_get_calculation_result_list():
    response = client.get('/calculation_results/', headers=researcher_auth_headers)
    assert response.status_code == 200

    cr = response.json()['items'][0]

    assert cr is not None
    assert cr['id'] == 1
    assert cr['user_id'] == 2
    assert cr['alpha'] == 1
    assert cr['beta'] == 1.2
    assert cr['mu'] == 0.3
    assert cr['g'] == 0.4
    assert cr['a'] == 3
    assert cr['n'] == 5
    assert cr['t1'] == 1
    assert cr['t2'] == 1
    assert cr['s'] == 1
    assert cr['calculated_at'] is not None