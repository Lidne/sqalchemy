import flask

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                                    'end_date', 'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'job': jobs.to_dict(only=(
                'id', 'team_leader', 'job', 'work_size', 'collaborators',
                'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/job_add', methods=['POST'])
def create_news():
    if not flask.request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in flask.request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'start_date',
                  'end_date', 'is_finished']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = Jobs(
        job=flask.request.json['job'],
        team_leader=flask.request.json['team_leader'],
        work_size=flask.request.json['work_size'],
        collaborators=flask.request.json['collaborators'],
        start_date=flask.request.json['start_date'],
        end_date=flask.request.json['end_date'],
        is_finished=flask.request.json['is_finished']
    )
    db_sess.add(job)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs_del/<int:job_id>', methods=['DELETE'])
def delete_news(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})
