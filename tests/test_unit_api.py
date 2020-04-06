from unittest import mock
from app import app


class MockPost:
    def __init__(self):
        self.title = "Title1"
        self.body = ""
        self.pub_date = "01.01.2020"

    def to_json(self):
        return {
            "title": self.title,
            "body": self.body,
            "date": self.pub_date
        }


def test_post_create():
    with app.app_context():
        with mock.patch("app.db.session.add") as add, \
                mock.patch("app.db.session.commit") as commit, \
                mock.patch("uuid.uuid4") as uuid:
            uuid.return_value = "123"
            r = app.test_client().post("/posts", data={
                "title": "Title1",
                "body": "qwdfwbeeta",
                "date": "01.01.2020"
            })
            add.assert_called_once()
            commit.assert_called_once()
    assert r.status_code == 201
    assert r.json['title'] == "Title1"
    assert r.json['uuid'] == "123"


def test_post_read_all():
    with mock.patch("app.db.session.query") as query:
        query.return_value.all.return_value = [MockPost(), MockPost()]
        r = app.test_client().get("/posts")
    assert r.status_code == 200
    assert len(r.json) == 2


def test_post_read():
    with mock.patch("app.db.session.query") as query:
        query.return_value.filter_by.return_value.first.return_value = MockPost()
        r = app.test_client().get("/posts/123")
    assert r.status_code == 200
    assert r.json['title'] == "Title1"


def test_post_read_not_found():
    with mock.patch("app.db.session.query") as query:
        query.return_value.filter_by.return_value.first.return_value = None
        r = app.test_client().get("/posts/123")
    assert r.status_code == 404


def test_post_update():
    data = {
        "title": "Title2",
        "body": "qwert",
        "date": "01.01.2021",
    }
    with mock.patch("app.db.session.query") as query, \
            mock.patch("app.db.session.add") as add, \
            mock.patch("app.db.session.commit") as commit:
        query.return_value.filter_by.return_value.first.return_value = MockPost()
        r = app.test_client().put('/posts/123', data=data)
    assert r.status_code == 200
    assert r.json == data


def test_post_put_not_found():
    with mock.patch("app.db.session.query") as query:
        query.return_value.filter_by.return_value.first.return_value = None
        r = app.test_client().put("/posts/123", data={})
    assert r.status_code == 404


def test_post_delete():
    with mock.patch("app.db.session.query") as query, \
            mock.patch("app.db.session.delete") as delete, \
            mock.patch("app.db.session.commit") as commit:
        query.return_value.filter_by.return_value.first.return_value = MockPost()
        r = app.test_client().delete('/posts/123')
    assert r.status_code == 204


def test_post_delete_not_found():
    with mock.patch("app.db.session.query") as query:
        query.return_value.filter_by.return_value.first.return_value = None
        r = app.test_client().delete("/posts/123")
    assert r.status_code == 404
