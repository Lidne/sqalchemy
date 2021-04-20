import requests
from data import db_session
from data.users import User
import random

try:
    db_session.global_init('db/mars_one.db')
    db_sess = db_session.create_session()
    users = list(map(lambda x: x.to_dict(only=(
        'surname', 'name', 'age', 'position', 'speciality',
        'address', 'email', 'hashed_password', 'modified_date'
    )), db_sess.query(User).all()))
    if not users:
        raise Exception
    res = requests.get('http://127.0.0.1:5000/api/users').json()['users']
    assert users == res
    for i in range(5):
        index = random.randint(1, len(users))
        res = requests.get(f'http://127.0.0.1:5000/api/users/{index}').json()['user']
        user = db_sess.query(User).filter(User.id == index).first().to_dict(only=(
            'surname', 'name', 'age', 'position', 'speciality',
            'address', 'email', 'hashed_password', 'modified_date'
        ))
        assert res == user
    index = len(users)
    user = db_sess.query(User).filter(User.id == index).first()
    res = requests.delete(f'http://127.0.0.1:5000/api/users/{index}').json()
    assert res['success'] == 'OK'
    assert not db_sess.query(User).filter(User.id == index).all()
    user_d = user.to_dict(only=(
        'surname', 'name', 'age', 'position', 'speciality',
        'address', 'email', 'hashed_password', 'modified_date'
    ))
    res = requests.post(f'http://127.0.0.1:5000/api/users', data=user_d).json()
    assert res['success'] == 'OK'
    print('Test passed')
except Exception as e:
    print('Test failed')
    print(e)
