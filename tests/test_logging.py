from typstwriter import typstwriter_logging
from re import match


def test_Message():
    """Test typstwriter_logging.Message."""
    assert str(typstwriter_logging.Message("A string: {}", ["Test"])) == "A string: Test"
    assert str(typstwriter_logging.Message("A debug string: {!r}", ["Test"])) == "A debug string: 'Test'"
    assert str(typstwriter_logging.Message("{} + {} = {}", [2, 2, 4])) == "2 + 2 = 4"


def test_StyleAdapter(caplog):
    """Test typstwriter_logging.StyleAdapter."""
    sa = typstwriter_logging.get_logger("test")

    sa.log(100, "A test")
    assert "A test" in caplog.text
    caplog.clear()

    sa.log(100, "A test with arguments: {}, {}", [1, 2, 3], "0")
    assert "A test with arguments: [1, 2, 3], 0" in caplog.text
    caplog.clear()

    sa.log(0, "A test")
    assert not caplog.text
    caplog.clear()


# This function does not use the caplog fixture directly because caplog injects
# its own handler in the typstwriter_logging and overrides the custom formatting.
# Instead the whole output is captured.
def test_setup_logger(capsys):
    """Test typstwriter_logging.getLogger."""
    typstwriter_logging.setup_logger("WARNING")
    logger = typstwriter_logging.get_logger("test")

    logger.critical("A test")
    (out, err) = capsys.readouterr()
    assert match(r"CRITICAL\s+\S+ \S+\s+test_logging.py\s+test_setup_logger\s+line \d+\s+: A test", err)

    logger.info("A test")
    (out, err) = capsys.readouterr()
    assert not out
    assert not err

    typstwriter_logging.setup_logger(level="Invalid")
    logger = typstwriter_logging.get_logger("test")

    logger.info("A test")
    (out, err) = capsys.readouterr()
    assert err == ""
    logger.warning("A test")
    (out, err) = capsys.readouterr()
    assert match(r"WARNING\s+\S+ \S+\s+test_logging.py\s+test_setup_logger\s+line \d+\s+: A test", err)
