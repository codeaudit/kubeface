import socket
from datetime import datetime
import getpass
import hashlib
import time

from .stringable import Stringable

JOB = Stringable(
    "Job",
    "{cache_key}::{node_id}::{randomness}")

TASK = Stringable(
    "Task",
    "{cache_key}::{task_num:06d}")

TASK_INPUT = Stringable(
    "TaskInput",
    "input::{task_name}")

TASK_RESULT = Stringable(
    "TaskResult",
    "result::{task_name}+{attempt_num:d}+{queue_time}+{result_time}+"
    "+{result_type}",
    valid_values={
        'result_type': ["value", "exception"],
    })

JOB_STATUS_PAGE = Stringable(
    "JobStatusPage",
    "{status}::{format}::{job_name}.{format}",
    valid_values={
        'format': ['html', 'json'],
        'status': ['active', 'done'],
    })

REMOTE_OBJECT = Stringable(
    "RemoteObject",
    "object::{cache_key_prefix}::{node_id}::{object_num:d}-{randomness}")


def hash_value(s, characters=8):
    return hashlib.sha1(str(s).encode()).hexdigest()[:characters]


def make_cache_key_prefix():
    cache_key_prefix = "%s-%s-%s-%s" % (
        socket.gethostname()[:8],
        getpass.getuser(),
        datetime.strftime(datetime.now(), "%Y-%m-%d-%H:%M:%S"),
        hash_value(time.time()))
    return cache_key_prefix


def make_job_name(cache_key, node_id):
    return JOB.make_string(
        cache_key=cache_key,
        node_id=node_id,
        randomness=hash_value(time.time()))


def make_remote_object_name(cache_key_prefix, node_id, object_num):
    return REMOTE_OBJECT.make_string(
        cache_key_prefix=cache_key_prefix,
        node_id=node_id,
        object_num=object_num,
        randomness=hash_value(time.time()))


def task_result_prefix(cache_key, task_names=[]):
    prefix = "result::" + cache_key
    if task_names:
        better_prefix = TASK_RESULT.prefix(task_name=list(task_names))
        assert better_prefix.startswith(prefix)
        return better_prefix
    return prefix


def task_input_prefix(cache_key):
    return "input::" + cache_key


def status_prefixes(job_names=None, formats=None, statuses=None):
    return JOB_STATUS_PAGE.prefixes(
        max_prefixes=4,
        job_name=job_names,
        format=formats,
        status=statuses)


def sanitize(name):
    return (
        name
        .replace(".", "-")
        .replace(":", "-")
        .replace("_", "-").lower())
