# coding:utf-8
# threading Timer: class threading.Timer(interval, function, args=[], kwargs={})
# 创建一个timer，在interval秒过去之后，它将以参数args和关键字参数kwargs运行function 。
#
# 2017-11-01: 现在start()可以做到判断定时触发的函数是否传递参数，从而兼容传入有参或无参的函数。
# 但因为有“repeat_times”参数在最后，也就是说如果想要控制有限次触发，则必须传入有参的函数，这算是一个不完美的地方

import sys
from threading import Timer


class JZTimer:

    def __init__(self):
        self._timer = None
        self._interval_second = 0
        self._on_time_func = None
        self._on_time_func_params = None
        self._repeat_times = 1

    _timer_input_no_value = object()

    def start(self, interval_second, on_time_func, on_time_func_params=_timer_input_no_value, repeat_times=sys.maxsize):
        self._interval_second = interval_second
        self._on_time_func = on_time_func
        self._repeat_times = repeat_times
        self._on_time_func_params = on_time_func_params
        self._run_timer()

    def stop(self):
        try:
            self._timer.cancel()
        except:
            pass

    def fire(self):
        self.stop()
        self._do_on_time_func()

    # private function

    def _run_timer(self):
        if self._repeat_times > 0:
            self._repeat_times -= 1
            self._timer = Timer(self._interval_second, self._do_on_time_func)
            self._timer.start()

    def _do_on_time_func(self):
        if self._on_time_func:
            if self._on_time_func_params is self._timer_input_no_value:
                self._on_time_func()
            else:
                self._on_time_func(self._on_time_func_params)

            self._run_timer()  # 重复运行

