import json


try:
    from langchain.tools import tool
except ImportError:
    class _SimpleTool:
        def __init__(self, func):
            self.func = func
            self.__name__ = func.__name__
            self.__doc__ = func.__doc__

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

        def invoke(self, input_value):
            return self.func(input_value)

    def tool(func):
        return _SimpleTool(func)


def build_tool_result(data, metadata=None, message=None):
    payload = data if isinstance(data, dict) else {"value": data}
    if message and "message" not in payload:
        payload = {**payload, "message": message}

    return json.dumps(
        {
            "status": "success",
            "data": payload,
            "metadata": metadata or {},
        },
        ensure_ascii=True,
    )


def build_tool_error(message, metadata=None):
    return json.dumps(
        {
            "status": "error",
            "data": {"message": message},
            "metadata": metadata or {},
        },
        ensure_ascii=True,
    )
