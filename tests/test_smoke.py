from zito.tracking import start_run


def test_null_tracker_does_not_raise():
    with start_run(run_name="smoke-test", config={"foo": "bar"}) as run:
        run.log({"ok": 1})
