import pytest
from mixer.backend.django import mixer

@pytest.mark.django_db
class TestModels:

    def test_comments_add(self):
        """ this test validates an comment model is created well """
        author = mixer.blend('accounts.CustomUser')
        comment = mixer.blend('comments.Comment', content='Very interesting and constructive comment.', author=author)
        assert comment.content == 'Very interesting and constructive comment.' and comment.author == author