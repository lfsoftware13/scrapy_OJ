DATABASE_PATH = 'data/scrapyOJ.db'
CODEDATA_PATH = 'release_data/'
SUBMIT = 'submit'
PROBLEM = 'problem'

CODEFORCE_DOMAIN = "http://codeforces.com"

problem_start_rediskey = "problem_spider:start_urls"
problem_error_rediskey = "problem_spider:error_urls"
problem_items_rediskey = "problem_spider:problem_items"

submit_start_rediskey = "submit_spider:start_urls"
submit_error_rediskey = "submit_spider:error_urls"
submit_cookidwait_rediskey = "submit_spider:cookie_wait_urls"
submit_items_rediskey = "submit_spider:submit_items"

code_start_rediskey = "code_spider:start_urls"
code_error_rediskey = "code_spider:error_urls"
code_items_rediskey = "code_spider:code_items"

code_notexist_items_rediskey = "code_spider:code_notexist_items"

problem_u_start_rediskey = "problem_u_spider:start_urls"
problem_u_error_rediskey = "problem_u_spider:error_urls"
problem_u_items_rediskey = problem_items_rediskey

submit_u_start_rediskey = "submit_u_spider:start_urls"
submit_u_error_rediskey = "submit_u_spider:error_urls"
submit_u_cookidwait_rediskey = "submit_u_spider:cookie_wait_urls"
submit_u_items_rediskey = submit_items_rediskey


problem_job = 'crawl_state/problem_spider'
submit_job = 'crawl_state/submit_spider'
code_job = 'crawl_state/code_spider'

problem_log = 'log/problem.log'
submit_log = 'log/submit.log'
code_log = 'log/code.log'
presis_log = 'log/presis.log'
problem_u_log = 'log/problem_update.log'
submit_u_log = 'log/submit_update.log'

problem_pid = 'pid/problem.pid'
submit_pid = 'pid/submit.pid'
code_pid = 'pid/code.pid'
presis_pid = 'pid/presis.pid'
problem_u_pid = 'pid/problem_update.pid'
submit_u_pid = 'pid/submit_update.pid'
