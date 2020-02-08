"""
Redis queue.
Created on {* now *}.
@desc: Redis queue views.
@app: {* app_name *}
"""
import logging
from app import appbuilder, rq
import requests
from app.models import MyUser

log = logging.getLogger(appbuilder.get_app.config['LOG_NAME'])


class JobExecuteException(Exception):
    """Customize exception for job execute. won't retry."""
    pass


class JobExecuteRetryException(Exception):
    """Customize exception for job execute. need retry."""
    pass


@rq.job(timeout=60 * 5, ttl=86400)
def schedule_requests_task(url, method, basic_auth, headers, **form):
    """do a task to raise request by the parameter url based on form."""
    try:
        res = requests.request(method, url, headers=headers, auth=basic_auth, data=form, verify=False, timeout=300)
        if res.status_code > 400:
            log.error('Failed schedule_requests_task job url={0} response={1}'.format(url, res.content))
            raise JobExecuteException('Failed schedule_requests_task job url={0} response={1}'.format(url, res.content))
        else:
            log.info('Successfully do schedule_requests_task job url={0} response={1}'.format(url, res.content))
    except Exception as e:
        log.error('Exception occrured  schedule_requests_task job url={0} response={1}'.format(url, e))
        raise JobExecuteException('Exception occrured  schedule_requests_task job url={0} response={1}'.format(url, e))


@rq.job(timeout=60, ttl=60)
def schedule_test_task(name):
    """do a test task to test flask-rq2 worker post fork."""
    # test touch the DB connection to see if got connection problem
    u1 = appbuilder.get_session.query(MyUser).filter(MyUser.id == 1).one_or_none()
    log.debug(u1)
    log.debug("schedule_test_task invoked say hi to {0}".format(name))
