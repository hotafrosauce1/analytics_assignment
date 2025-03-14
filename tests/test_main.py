import requests as r
import os
import time

if __name__ == '__main__':
    post_request_data = [
      {"user_id": 101, "timestamp": "2025-01-01T09:45:00Z", "heart_rate": 82, "steps": 300, "calories": 13},
      {"user_id": 202,"timestamp": "2025-01-01T10:00:00Z", "heart_rate": 90,"steps": 500,"calories": 22.5},
      {"user_id": 101,"timestamp": "2025-01-01T10:15:00Z", "heart_rate": 85,"steps": 200,"calories": 9.1},
      {"user_id": 101,"timestamp": "2025-01-01T09:30:00Z", "heart_rate": 78,"steps": 150,"calories": 6.5}
    ]

    fastapi_host = os.getenv('FASTAPI_HOST')
    fastapi_port = os.getenv('FASTAPI_PORT')

    get_url = f'http://{fastapi_host}:{fastapi_port}/metrics'
    post_url = f'http://{fastapi_host}:{fastapi_port}/ingest'

    # Make several POST requests to the server
    for data in post_request_data:
        print('Sending POST request with data:', data)
        print()
        post_response = r.post(post_url, json = data)
        assert post_response.json() == {'message': 'Data received'}

    print('All POST requests sent!')
    print()

    # Wait a bit for the Celery worker to process the POST requests
    time.sleep(5)

    # Make a valid GET request to the server
    print('Sending GET request to the server for user_id 101 between 2025-01-01T09:00:00Z and 2025-01-01T11:00:00Z')
    print()
    get_params = {'user_id': 101, 'start_date': '2025-01-01T09:00:00Z', 'end_date': '2025-01-01T11:00:00Z'}
    get_response = r.get(get_url, params = get_params)

    assert get_response.status_code == 200
    assert get_response.json() == {'avg_heart_rate': 81.66666666666667, 'total_steps': 650, 'total_calories': 28.6}

    # Make a GET request with invalid date range
    print('Sending GET request to the server for user_id 101 between 2025-01-01T12:00:00Z and 2025-01-01T13:00:00Z')
    print()
    get_params = {'user_id': 101, 'start_date': '2025-01-01T12:00:00Z', 'end_date': '2025-01-01T13:00:00Z'}
    get_response = r.get(get_url, params = get_params)

    assert get_response.status_code == 404
    assert get_response.json() == {'detail': 'No data found for the given user and date range'}

    # Make a GET request with invalid user_id
    print('Sending GET request to the server for invalid user_id 999 between 2025-01-01T09:00:00Z and 2025-01-01T11:00:00Z')
    print()
    get_params = {'user_id': 999, 'start_date': '2025-01-01T09:00:00Z', 'end_date': '2025-01-01T11:00:00Z'}
    get_response = r.get(get_url, params = get_params)

    assert get_response.status_code == 404
    assert get_response.json() == {'detail': 'No data found for the given user and date range'}

    # Make a GET request with invalid argument types
    print('Sending GET request to the server with invalid argument types')
    print()
    get_params = {'user_id': 'invalid', 'start_date': 'invalid', 'end_date': 'invalid'}
    get_response = r.get(get_url, params = get_params)

    assert get_response.status_code == 422
    assert get_response.json() == {'detail': [{'type': 'int_parsing', 'loc': ['query', 'user_id'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'invalid'}, {'type': 'datetime_from_date_parsing', 'loc': ['query', 'start_date'], 'msg': 'Input should be a valid datetime or date, input is too short', 'input': 'invalid', 'ctx': {'error': 'input is too short'}}, {'type': 'datetime_from_date_parsing', 'loc': ['query', 'end_date'], 'msg': 'Input should be a valid datetime or date, input is too short', 'input': 'invalid', 'ctx': {'error': 'input is too short'}}]}

    # Make a GET request with missing arguments
    print('Sending GET request to the server with missing arguments')
    print()
    get_params = {'user_id': 101, 'start_date': '2025-01-01T09:00:00Z'}
    get_response = r.get(get_url, params = get_params)

    assert get_response.status_code == 422
    assert get_response.json() == {'detail': [{'type': 'missing', 'loc': ['query', 'end_date'], 'msg': 'Field required', 'input': None}]}

    # Make a POST request with invalid argument types
    print('Sending POST request to the server with invalid argument types')
    print()
    post_request_data = {'user_id': 'invalid', 'timestamp': '2025-01-01T09:45:00Z', 'heart_rate': 82, 'steps': 300, 'calories': 13}
    post_response = r.post(post_url, json = post_request_data)

    assert post_response.status_code == 422
    assert post_response.json() == {'detail': [{'type': 'int_parsing', 'loc': ['body', 'user_id'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'invalid'}]}

    # Make a POST request with missing arguments
    print('Sending POST request to the server with missing arguments')
    print()
    post_request_data = {'user_id': 101, 'timestamp': '2025-01-01T09:45:00Z', 'heart_rate': 82, 'calories': 13}
    post_response = r.post(post_url, json = post_request_data)

    assert post_response.status_code == 422
    assert post_response.json() == {'detail': [{'type': 'missing', 'loc': ['body', 'steps'], 'msg': 'Field required', 'input': {'user_id': 101, 'timestamp': '2025-01-01T09:45:00Z', 'heart_rate': 82, 'calories': 13}}]}

    print("All tests passed!")