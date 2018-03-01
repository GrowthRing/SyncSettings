import requests
import json
from functools import wraps


class NotFoundError(RuntimeError):
    pass


class UnexpectedError(RuntimeError):
    pass


class NetworkError(RuntimeError):
    pass


class AuthenticationError(RuntimeError):
    pass


class UnprocessableDataError(RuntimeError):
    pass


def auth(func):
    @wraps(func)
    def auth_wrapper(self, *args, **kwargs):
        if self.token is None:
            raise AuthenticationError("GitHub's credentials are required")
        return func(self, *args, **kwargs)
    return auth_wrapper


class Gist:
    def __init__(self, token=None, **kwargs):
        self.token = token
        self._params = kwargs

    @staticmethod
    def make_uri(endpoint=None):
        url = ['https://api.github.com', 'gists']
        if endpoint:
            url.append(endpoint)
        return '/'.join(url)

    @auth
    def create(self, data):
        if not len(data):
            raise ValueError("Gist can't be created without data")
        return self.__do_request('post', self.make_uri(), data=json.dumps(data)).json()

    @auth
    def update(self, data, gist_id):
        if not len(data):
            raise ValueError("Gist can't be updated without data")

        if not gist_id:
            raise ValueError("The given id is not valid")

        return self.__do_request('patch', self.make_uri(gist_id), data=json.dumps(data)).json()

    @auth
    def delete(self, gist_id):
        if not gist_id:
            raise ValueError("The given id is not valid".format(gist_id))
        response = self.__do_request('delete', self.make_uri(gist_id))
        return response.status_code == 204

    def get(self, gist_id):
        if not gist_id:
            raise ValueError("The given id is not valid".format(gist_id))

        def get_raw_content(url):
            return self.__do_request('get', url).content

        data = self.__do_request('get', self.make_uri(gist_id)).json()
        for file_name, file_data in data['files'].items():
            if file_data['truncated']:
                raw_content = get_raw_content(file_data['raw_url'])
                file_data['content'] = raw_content if raw_content else file_data['content']

        return data

    def __do_request(self, verb, url, **kwargs):
        try:
            response = getattr(requests, verb)(url, headers=self.headers, **{**self._params, **kwargs})
        except requests.exceptions.ConnectionError:
            raise NetworkError("Can't perform this action due to network errors")

        if response.status_code == 404:
            raise NotFoundError("The requested resource do not exists")

        if response.status_code == 401:
            raise AuthenticationError("The given credentials are not valid")

        if response.status_code == 422:
            raise UnprocessableDataError("The provided data has errors")

        if response.status_code >= 300:
            raise UnexpectedError("Unexpected Error, Reason: {}".format(response.json()['message']))

        return response

    @property
    def headers(self):
        if self.token is None:
            return {}

        return {
            'Content-Type': 'application/json',
            'Authorization': 'token {}'.format(self.token)
        }
