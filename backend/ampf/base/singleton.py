singleton_instances = {}


def singleton(cls):
    def get_instance(*args, **kwargs):
        if cls not in singleton_instances:
            singleton_instances[cls] = cls(*args, **kwargs)
        return singleton_instances[cls]

    return get_instance
