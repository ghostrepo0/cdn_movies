import asyncio
from functools import partial, wraps


def backoff(func=None, start_sleep_time=0.1, factor=2, border_sleep_time=10, logger=None):
    """
    Функция для повторного выполнения функции через некоторое время,
     если возникла ошибка. Использует наивный экспоненциальный рост времени повтора (factor) до
      граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param func: необходим чтобы "декорировать без скобочек"
    :param logger: logger object logger=logging.getLogger(__name__)
    :return: результат выполнения функции
    """
    if not func:
        return partial(backoff, start_sleep_time=start_sleep_time,
                       factor=factor, border_sleep_time=border_sleep_time, logger=logger)

    @wraps(func)
    async def func_wrapper(*args, **kwargs):
        attempt = 0
        sleep_time = start_sleep_time
        while True:
            try:
                return await func(*args, **kwargs)
            except Exception:
                attempt += 1
                time_gap = sleep_time + start_sleep_time * 2 ** factor
                sleep_time = time_gap if time_gap < border_sleep_time else border_sleep_time
                exception_massage = f'Exception thrown when attempting to run {func}, attempt {attempt}.'\
                                    f'Retrying in {sleep_time:.2f} sec.'
                if logger:
                    logger.warning(exception_massage)
                else:
                    print(exception_massage)

                await asyncio.sleep(sleep_time)

    return func_wrapper
