from quart_openapi import Pint, Resource
from quart import request, jsonify
app = Pint(__name__, title='Sample App')


expected = app.create_validator('sample_request', {
    'type': 'object',
    'properties': {
        'word': {
            'type': 'string'
        },
        'urls': {
            'type': 'array',
            'items': {'type': 'string'}
        }
    }
})


@app.route('/')
class Root(Resource):
    @app.expect(expected)
    async def post(self):
        '''Counts the number of times which a given word appear in each site.
        '''
        data = await request.get_json()
        return jsonify(data)
