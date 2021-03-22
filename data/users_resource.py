import flask
import flask_restful
from data import db_session
from data.parser import parser
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        flask.abort(404)


class UsersResource(flask_restful.Resource):

    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return flask.jsonify({'user': user.to_dict(
            only=(
                'surname', 'name', 'age', 'position', 'speciality',
                'address', 'email', 'hashed_password', 'modified_date'
            ))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return flask.jsonify({'success': 'OK'})


class UsersListResource(flask_restful.Resource):

    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return flask.jsonify({'users': [item.to_dict(
            only=(
                'surname', 'name', 'age', 'position', 'speciality',
                'address', 'email', 'hashed_password', 'modified_date'
            )) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password'],
            modified_date=args['modified_date']
        )
        session.add(user)
        session.commit()
        return flask.jsonify({'success': 'OK'})
