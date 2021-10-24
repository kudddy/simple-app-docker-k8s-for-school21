from aiohttp.web_urldispatcher import DynamicResource


def url_for(path: str, **kwargs) -> str:
    """
    Генерирует URL для динамического aiohttp маршрута с параметрами.
    """
    kwargs = {
        key: str(value)  # Все значения должны быть str (для DynamicResource)
        for key, value in kwargs.items()
    }
    return str(DynamicResource(path).url_for(**kwargs))
