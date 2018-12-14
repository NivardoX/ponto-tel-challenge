import pytest
from api import app


@pytest.fixture(name='test_app')
def _test_app(tmpdir):
    return app


@pytest.mark.asyncio
async def test_create(test_app):
    test_client = test_app.test_client()
    response = await test_client.post(
        '/', json={'word': 'google',
                   'urls': ['https://www.google.com',
                            'https://www.youtube.com']}
    )
    assert response.status_code == 200
