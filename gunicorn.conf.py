import multiprocessing
from tempfile import mkdtemp


# ===============================================
#           Server Socket
# ===============================================

# 소켓 바인딩, host:port 형식의 문자열
bind = "0.0.0.0:8000"

# 대기중인 최대 연결 수, 64~2048
backlog = 2048


# ===============================================
#           Worker Processes
# ===============================================

# request를 처리하는 worker 프로세스 개수
# 일반적으로 2~4 x 프로세스 코어 개수로 설정
workers = multiprocessing.cpu_count() * 2 + 1

# 워커의 종류를 의미하는 문자열
# Union["sync", "eventlet", "gevent", "tornado", "gthread", "uvcorn"]
# http://docs.gunicorn.org/en/latest/design.html
worker_class = "sync"

# request를 처리하는 worker의 스레드 개수
threads = 1

# eventlet, gevent 전용, 최대 동시 클라이언트 수
worker_connections = 1000

# worker가 재시작 되기 전 처리할 최대 요청 수
max_requests = 10000

# max_requests 설정에 영향을 주는 값
# worker의 재시작이 randint(0, max_requests_jitter)로 인해 무작위화
# worker간의 재시작 시차를 두기 위한 속성
max_requests_jitter = 1000

# timeout초 이상 응답이 없는 worker를 종료시키고 재시작
timeout = 30

# worker가 restart 신호를 받은 후 request를 처리할 수 있는 최대 시간
# 해당 시간이 넘어갈 경우 worker는 강제 kill
graceful_timeout = 30

# keep-alive 연결이 request를 기다리는 시간, 일반적으로 1~5
keep_alive = 2


# ===============================================
#           Security
# ===============================================

# http request의 최대 byte 크기, 0(inf)~8190, ddos 공격 방지
limit_request_line = 1024

# http request 헤더의 최대 필드 수, 0(inf)~32768, ddos 공격 방지
limit_request_fields = 100

# http request 헤더의 최대 byte 크기, 0(inf)~8190
limit_request_field_size = 1024


# ===============================================
#           Debugging
# ===============================================

# 코드 변경 시 worker restart
reload = True

# gunicorn의 재시작을 수행하는 타입
# Union["auto", "poll", "inotify"]
reload_engine = "auto"

# reload 시 다시 load하도록 하는 추가적인 대상들
# Union["templates", "configurations", "specifications", ...]
reload_extra_files = []

# 서버가 실행하는 모든 line을 stdout으로 출력하는 기능
spew = False

# config 체크
check_config = False


# ===============================================
#           Server Mechanics
# ===============================================

# worker가 분기되기 전 app code를 load하는지의 여부
# app을 미리 load하여 일무 ram 자원을 절약하고 서버 boot 시간을 단축할 수 있다.
preload_app = True

# sendfile 활성화 여부
sendfile = False

# SO_REUSEPORT 활성화 여부
reuse_port = False

# chdir - app을 load하기 전 해당 path로 이동
chdir = ""

# gunicorn 프로세스를 백그라운드에서 실행할지의 여부
daemon = False

# 환경변수 설정, key=value 형식의 문자열
raw_env = []

# pid의 파일 이름으로 사용될 문자열, 없으면 pid 파일을 기록하지 않음
pidfile = None

# worker가 사용하는 임시 파일 디렉토리 이름, 없다면 기본 임시 디렉토리
worker_tmp_dir = mkdtemp(prefix="gunicorn_")

# worker 프로세스를 실행할 user, user ID(int) 또는 None
user = None

# worker 프로세스를 실행할 group, group ID(int) 또는 None
group = None

# gunicorn이 작성한 파일의 mode에 대한 비트 마스크
umask = 0

# initgroups - If true, set the worker process’s group access list with all of
# the groups of which the specified username is a member, plus the specified
# group id.
initgroups = False

# 임시 request data를 저장할 때 사용되는 디렉토리, worker가 쓰기 가능해야 함
# None일 경우 시스템이 생성하는 임시 디렉토리를 사용
tmp_upload_dir = None

# 프론트엔드 프록시가 HTTPS request를 표현하는데에 사용하는 dict
# gunicorn이 wsgi.url_schema를 https로 설정하도록 지시한다
secure_scheme_headers = {
    "X-FORWARDED-PROTOCOL": "ssl",
    "X-FORWARDED-PROTO": "https",
    "X-FORWARDED-SSL": "on",
}

# front-end 접근 허용 ips, ","로 구분, "*" 설정 가능
forwarded_allow_ips = "127.0.0.1"

# python path에 추가될 dir paths, ","로 구분
pythonpath = None

# paste - Load a PasteDeploy config file. The argument may contain a # symbol
# followed by the name of an app section from the config file,
# e.g. production.ini#admin.
# At this time, using alternate server blocks is not supported. Use the command
# line arguments to control server configuration instead.
paste = None

# proxy_protocol - Enable detect PROXY protocol (PROXY mode).
# Allow using Http and Proxy together. It may be useful for work with stunnel
# as https frontend and gunicorn as http server.
# PROXY protocol: http://haproxy.1wt.eu/download/1.5/doc/proxy-protocol.txt
proxy_protocol = False

# proxy front-end 접근 허용 ips, ","로 구분, "*" 설정 가능
proxy_allow_ips = "127.0.0.1"

# raw_paste_global_conf - Set a PasteDeploy global config variable in key=value
# form.
# The option can be specified multiple times.
# The variables are passed to the the PasteDeploy entrypoint. Example:
# $ gunicorn -b 127.0.0.1:8000 --paste development.ini --paste-global FOO=1
# --paste-global BAR=2
raw_paste_global_conf = []

# 헤더 key와 ":" 사이의 공백 제거, 취약, 필요한 경우에만 주의하여 활용
strip_header_spaces = False


# ===============================================
#           SSL
# ===============================================

# ssl key file
keyfile = None

# SSL 증명 file
certfile = None

# 사용할 SSL 버전을 의미하는 문자열
# "TLS" - tls 버전을 협상하여 선택, Python 3.6 이상
# "TLSv1" - TLS 1.0
# "TLSv1_1" - TLS 1.1, Python 3.4 이상
# "TLSv1_2"  TLS 1.2, Python 3.4 이상
# "TLS_SERVER" - TLS와 유사하나 서버측 SSLSocket 연결만 지원
ssl_version = "TLSv1_2"

# 클라이언트 인증서 필요 여부 (see stdlib ssl module’s)
cert_reqs = 0

# CA 증명 file path
ca_certs = None

# suppress_ragged_eofs - Suppress ragged EOFs (see stdlib ssl module’s)
suppress_ragged_eofs = True

# 소켓 연결에 SSL handshake를 수행할 지의 여부
do_handshake_on_connect = False

# OpenSSL 암호로 사용할 문자열 목록
ciphers = None


# ===============================================
#           Logging
# ===============================================

# 액세스 로그 파일 path, "-"로 설정시 stdout
accesslog = "-"

# 액세스 로그 포멧 설정 문자열
# Identifier  |  Description
# ------------------------------------------------------------
# h            ->  remote address
# l            -> ‘-‘
# u            -> user name
# t            -> date of the request
# r            -> status line (e.g. GET / HTTP/1.1)
# m            -> request method
# U            -> URL path without query string
# q            -> query string
# H            -> protocol
# s            -> status
# B            -> response length
# b            -> response length or ‘-‘ (CLF format)
# f            -> referer
# a            -> user agent
# T            -> request time in seconds
# D            -> request time in microseconds
# L            -> request time in decimal seconds
# p            -> process ID
# {header}i    -> request header
# {header}o    -> response header
# {variable}e  -> environment variable
# ---------------------------------------------------------------
# Use lowercase for header and environment variable names, and put {...}x names
# inside %(...)s. For example:
# %({x-forwarded-for}i)s
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# redirection access log 비활성화 여부
disable_redirect_access_to_syslog = False

# error 로그 파일 path, "-"로 설정시 stdout
errorlog = "-"

# error 로그 출력 레벨
# "debug" > "info" > "worning" > "error" > "critical"
loglevel = "info"

# capture_output - Redirect stdout/stderr to specified file in errorlog.
capture_output = False

# 로그를 기록하는데에 사용되는 로거
logger_class = "gunicorn.glogging.Logger"

# 로그 config 파일, Python Logging 모듈의 config 형식을 사용
logconfig = None

# 로그 설정, logconfig 보다 높은 우선순위
# https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig
logconfig_dict = {}

# syslog_addr - Address to send syslog messages.
#
# Address is a string of the form:
# ‘unix://PATH#TYPE’ : for unix domain socket. TYPE can be ‘stream’ for the
#                      stream driver or ‘dgram’ for the dgram driver.
#                      ‘stream’ is the default.
# ‘udp://HOST:PORT’ : for UDP sockets
# ‘tcp://HOST:PORT‘ : for TCP sockets
syslog_addr = "udp://localhost:514"

# Gunicorn log를 syslog에 전송할지의 여부
syslog = False

# syslog_prefix - Makes gunicorn use the parameter as program-name in the
# syslog entries.
# All entries will be prefixed by gunicorn.<prefix>. By default the program
# name is the name of the process.
syslog_prefix = None

# syslog_facility - Syslog facility name
syslog_facility = "user"

# enable_stdio_inheritance - Enable stdio inheritance
# Enable inheritance for stdio file descriptors in daemon mode.
# Note: To disable the python stdout buffering, you can to set the user
# environment variable PYTHONUNBUFFERED .
enable_stdio_inheritance = False

# statsd_host - host:port of the statsd server to log to
statsd_host = None

# statsd_prefix - Prefix to use when emitting statsd metrics (a trailing . is
# added, if not provided)
statsd_prefix = ""

# dogstatsd_tags - A comma-delimited list of datadog statsd (dogstatsd) tags to
# append to statsd metrics.
dogstatsd_tags = ""


# ===============================================
#           Process Naming
# ===============================================

# 사용할 gunicorn 프로세스 이름
proc_name = "gunicorn"


# ===============================================
#           Server Hooks
# ===============================================


def on_starting(server):
    """
    Execute code just before the main process is initialized.
    The callable needs to accept a single instance variable for the Arbiter.
    """


def on_reload(server):
    """
    Execute code to recycle workers during a reload via SIGHUP.
    The callable needs to accept a single instance variable for the Arbiter.
    """


def when_ready(server):
    """
    Execute code just after the server is started.
    The callable needs to accept a single instance variable for the Arbiter.
    """


def pre_fork(server, worker):
    """
    Execute code just before a worker is forked.
    The callable needs to accept two instance variables for the Arbiter and
    new Worker.
    """


def post_fork(server, worker):
    """
    Execute code just after a worker has been forked.
    The callable needs to accept two instance variables for the Arbiter and
    new Worker.
    """


def post_worker_init(worker):
    """
    Execute code just after a worker has initialized the application.
    The callable needs to accept one instance variable for the initialized
    Worker.
    """


def worker_int(worker):
    """
    Execute code just after a worker exited on SIGINT or SIGQUIT.
    The callable needs to accept one instance variable for the initialized
    Worker.
    """


def worker_abort(worker):
    """
    Execute code when a worker received the SIGABRT signal.
    This call generally happens on timeout.
    The callable needs to accept one instance variable for the initialized
    Worker.
    """


def pre_exec(server):
    """
    Execute code just before a new main process is forked.
    The callable needs to accept a single instance variable for the Arbiter.
    """


def pre_request(worker, req):
    """
    Execute code just before a worker processes the request.
    The callable needs to accept two instance variables for the Worker and
    the Request.
    """
    worker.log.debug("%s %s", req.method, req.path)


def post_request(worker, req, environ, resp):
    """
    Execute code after a worker processes the request.
    The callable needs to accept two instance variables for the Worker and
    the Request.
    """


def child_exit(server, worker):
    """
    Execute code just after a worker has been exited, in the main process.
    The callable needs to accept two instance variables for the Arbiter and the
    just-exited Worker.
    """


def worker_exit(server, worker):
    """
    Execute code just after a worker has been exited.
    The callable needs to accept two instance variables for the Arbiter and
    the just-exited Worker.
    """


def nworkers_changed(server, new_value, old_value):
    """
    Execute code just after num_workers has been changed.
    The callable needs to accept an instance variable of the Arbiter and two
    integers of number of workers after and before change.
    If the number of workers is set for the first time, old_value would be
    None.
    """


def on_exit(server):
    """
    Execute code just before exiting gunicorn.
    The callable needs to accept a single instance variable for the Arbiter.
    """
