import requests
import json
import logging

URL = "http://13.233.156.224/"


def post_endpoint_with_data(endpoint, **kwargs):
    url = URL + endpoint + "/"
    headers = {"Content-Type": "application/json"}

    data = kwargs

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes
        return (response.json())
    except requests.exceptions.RequestException as e:
        logging.exception(f"An error occurred: {e}")
    except json.JSONDecodeError as e:
        logging.exception(f"Error decoding JSON response: {e}")
        logging.exception(f"Raw response text: {response.text}")


def get_endpoint_with_params(endpoint, **kwargs):
    url = URL + endpoint + "/"
    params = kwargs

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.exception(f"An error occurred: {e}")
    except json.JSONDecodeError as e:
        logging.exception(f"Error decoding JSON response: {e}")




END_POINT_POST = "post_graph_invoke"
END_POINT_GET = "get_evaluation"


def get_interview(data):


    print(data)

    result = post_endpoint_with_data(END_POINT_POST, **data)
    policy_violation = result['policy_violation']
    new_question = None
    num_questions = None

    if policy_violation != "NA":
        return  policy_violation

    else:
        new_question = result['new_question']
        num_questions = result['num_questions']

    if data['num_questions'] >= data['max_questions']:
        return None

    return policy_violation, new_question, num_questions


def get_evaluation(unique_id):
    return  get_endpoint_with_params(END_POINT_GET, user_id=str(unique_id))