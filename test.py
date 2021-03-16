import requests
from data import db_session
from data.jobs import Jobs

# получение всех работ
try:
    api_job = requests.get('http://127.0.0.1:5000/api/jobs').json()
    db_session.global_init('db/mars_one.db')
    db_sess = db_session.create_session()
    all_jobs = {
        'jobs':
            [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                                'end_date', 'is_finished'))
             for item in db_sess.query(Jobs).all()]
    }

    for key, item in all_jobs.items():
        if api_job[key] != item:
            raise Exception

    for key, item in api_job.items():
        if all_jobs[key] != item:
            raise Exception

    print('Test 1: ok')
except Exception as e:
    print('Test 1: failed')
    print('Error:', e)

# получение одной работы
try:
    db_sess = db_session.create_session()
    all_jobs = list(
        item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                           'end_date', 'is_finished'))
        for item in db_sess.query(Jobs).all()
    )

    for i in range(len(all_jobs)):
        api_job = requests.get('http://127.0.0.1:5000/api/jobs/{}'.format(i + 1)).json()['job']

        if all_jobs[i] != api_job:
            raise Exception

    print('Test 2: ok')
except Exception as e:
    print('Test 2: failed')
    print('Error:', e)


try:
    # проверка на ошибку: неправильный индекс
    api_resp = requests.get('http://127.0.0.1:5000/api/jobs/0').json()
    assert 'error' in api_resp
    api_resp = requests.get('http://127.0.0.1:5000/api/jobs/999').json()
    assert 'error' in api_resp
    print('Test 3: ok')
    # проверка на ошбку: буквы в запросе
    api_resp = requests.get('http://127.0.0.1:5000/api/jobs/wd').json()
    if 'error' not in api_resp:
        raise ValueError
    print('Test 4: ok')
except AssertionError:
    print('Test 3: failed')
except ValueError:
    print('Test 4: failed')
