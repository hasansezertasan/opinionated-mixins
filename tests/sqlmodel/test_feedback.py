from opinionated_mixins.contrib.sqlmodel import Feedback


class TestSQLModelFeedback:
    def test_reexports_sqlalchemy(self) -> None:
        from opinionated_mixins.contrib.sqlalchemy import Feedback as SAFeedback

        assert Feedback is SAFeedback
