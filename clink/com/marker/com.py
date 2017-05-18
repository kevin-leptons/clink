from clink.com.injector import CLINK_COM_ATTR


def com(*args):
    def decorator_fn(target_obj):
        if CLINK_COM_ATTR in dir(target_obj):
            target_obj.__clink['req_coms'] = args
        else:
            target_obj.__clink = {'req_coms': args }
        return target_obj
    return decorator_fn
