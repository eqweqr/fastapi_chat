from tasks import sleep_and_print, print_hel
from celery.result import AsyncResult
import time
from unittest.mock import patch
from unittest import TestCase

# x = sleep_and_print.delay()
# task_id = x.task_id
# res = AsyncResult(task_id).status
# print(res)
# time.sleep(2)
# res = AsyncResult(task_id).status
# print(res)

# @patch('tasks.sleep_and_print', side_effect=mocked_post)
# def test_task():
#     assert sleep_and_print.run()
#     assert sleep_and_print.run.call_count == 2
class MyTest(TestCase):

    @patch('tasks.sleep_and_print.run')
    def test_foo(self, post_mock):
        assert sleep_and_print.run()
        post_mock.assert_called_once_with()

        assert sleep_and_print.run()
        assert post_mock.call_count == 2
        # assert sleep_and_print.run.
                # assert post_mock.
        # post_mock.return_value = 3

    @patch('tasks.time')
    def test_sleep(self, post_mock):
        sleep_and_print.run()
        assert post_mock.sleep.called
        post_mock.sleep.assert_called_once_with(1)