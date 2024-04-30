"""
    Two ways of printing exception traceback
"""


try:
    1 / 0
except Exception as e:
    import logging; logging.getLogger("some-name").error(str(e), exc_info=True)
    import traceback; print(traceback.format_exc())
