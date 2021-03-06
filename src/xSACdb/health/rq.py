

import time

from django.conf import settings
from django_rq import enqueue, get_scheduler
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceReturnedUnexpectedResult, ServiceUnavailable


def add(a, b):
    return a + b

class RQWorkerHealthCheck(BaseHealthCheckBackend):
    def check_status(self):
        timeout = time.time() + getattr(settings, 'HEALTHCHECK_RQWORKER_TIMEOUT', 4)

        try:
            job = enqueue(add, 5, 6)
            while True:
                if job.result or time.time() > timeout:
                    break
            if not job.result:
                self.add_error(ServiceUnavailable("No result, are workers running?"))
            elif job.result == '11':
                self.add_error(ServiceReturnedUnexpectedResult("Invalid result"))
        except BaseException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)


class RQSchedulerHealthCheck(BaseHealthCheckBackend):
    def check_status(self):
        try:
            scheduler = get_scheduler('default')
            if not scheduler:
                self.add_error(ServiceUnavailable("No scheduler"))
            if scheduler.count() == 0:
                self.add_error(ServiceUnavailable("No jobs in scheduler"))
        except BaseException as e:
            self.add_error(ServiceUnavailable("Unknown error"), e)
            raise(e)
