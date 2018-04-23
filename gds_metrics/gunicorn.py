from prometheus_client import multiprocess  # pragma: no cover


def child_exit(server, worker):  # pragma: no cover
    multiprocess.mark_process_dead(worker.pid)  # pragma: no cover
