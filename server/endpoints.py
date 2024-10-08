"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from http import HTTPStatus

from flask import Flask, request  # , request
from flask_restx import Resource, Api, fields  # Namespace, fields
from flask_cors import CORS

import werkzeug.exceptions as wz

import data.users as usr

app = Flask(__name__)
CORS(app)
api = Api(app)

ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'

HELLO_EP = '/hello'
HELLO_RESP = 'hello'

JOURNAL_NAME_EP = '/journalname'
JOURNAL_NAME_RESP = 'Journal Name'
JOURNAL_NAME = 'team-asare-fall-2024'

USERS_EP = '/user'
USERS_RESP = 'Message'
RETURN = 'return'


USER_CREATE_FLDS = api.model('AddNewUserEntry', {
    usr.NAME: fields.String,
    usr.EMAIL: fields.String,
    usr.AFFILIATION: fields.String
})


@api.route(f'{USERS_EP}/create')
class UserCreate(Resource):
    """
    Add a user to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(USER_CREATE_FLDS)
    def put(self):
        """
        Add a user.
        """
        try:
            name = request.json.get(usr.NAME)
            email = request.json.get(usr.EMAIL)
            affiliation = request.json.get(usr.AFFILIATION)
            ret = usr.create(name, email, affiliation)
        except Exception as err:
            raise wz.NotAcceptable(f'Count not add user: '
                                   f'{err=}')
        return {
            USERS_RESP: 'User added!',
            RETURN: ret,
        }


@api.route(JOURNAL_NAME_EP)
class JournalName(Resource):
    """
    The purpose of JournalName is to have a simple test to output
    the journal name.
    """
    def get(self):
        """
        An endpoint made for 'Group Dev Env Working' assignment.
        It just answers with "team-asare-fall-2024"
        """
        return {JOURNAL_NAME_RESP: JOURNAL_NAME}


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return sorted a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {ENDPOINT_RESP: endpoints}
