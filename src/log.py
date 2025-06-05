import os
import sys
import logging
import inspect

logging.basicConfig(format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
log = logging.getLogger('drinkbot')
log.setLevel(logging.INFO)


def log_detail( msg ):
    stack = inspect.stack()[1]
    file = os.path.basename( stack[1] )
    msg =  'Error: {} @ {}:{}'.format (msg, file, stack[2] )
    print(msg)
    return msg


if __name__ == "__main__":
    pass