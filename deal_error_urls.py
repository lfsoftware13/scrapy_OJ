from redis_database.redis_util import list_push_left, list_pop, llendb
from database.constants import problem_error_rediskey, problem_start_rediskey, submit_error_rediskey, submit_start_rediskey, code_error_rediskey, code_start_rediskey, problem_u_error_rediskey, problem_u_start_rediskey, submit_u_error_rediskey, submit_u_start_rediskey
from util.ScriptsUtil import initLogging
import logging
import logging

def move_error_to_start(error_rediskey, startrediskey):
    cou = llendb(error_rediskey)
    if cou > 0:
        err = list_pop(error_rediskey)
        if err:
            list_push_left(startrediskey, err)
    logging.info('[ERROR_MOVE]['+str(cou)+']['+error_rediskey+']['+startrediskey+']')


def move():
    initLogging()
    move_error_to_start(problem_error_rediskey, problem_start_rediskey)
    move_error_to_start(submit_error_rediskey, submit_start_rediskey)
    move_error_to_start(code_error_rediskey, code_start_rediskey)
    move_error_to_start(problem_u_error_rediskey, problem_u_start_rediskey)
    move_error_to_start(submit_u_error_rediskey, submit_u_start_rediskey)

move()

