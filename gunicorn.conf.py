bind = "127.0.0.1:5000"

workers = 2

worker_class = "sync"

timeout = 120
graceful_timeout = 30
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = "info"

capture_output = True

preload_app = False

max_requests = 1000
max_requests_jitter = 100

proc_name = "sumber-aquarium"

umask = 0o007

worker_tmp_dir = "/dev/shm"
