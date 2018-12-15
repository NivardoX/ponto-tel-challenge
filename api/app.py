import crawler
import validators
from quart_openapi import Pint, Resource
from quart import request, jsonify
from marshmallow import Schema, fields
app = Pint(__name__, title='Sample App')


class CountSchema(Schema):
    word = fields.String(required=True)
    urls = fields.List(fields.Str(), required=True)


expected = app.create_validator('sample_request', {
    'type': 'object',
    'properties': {
        'word': {
            'type': 'string'
        },
        'urls': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
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
        result, errors = CountSchema().load(data)

        # check if params were receive
        if errors != {}:
            errors.update({'success': False})
            return jsonify(errors)

        # check with all are urls
        for url in result['urls']:
            if not validators.url(url):
                errors.update({"urls": "not all are urls"})
                errors.update({'success': False})
                return jsonify(errors)

        # with all params are ok, than count
        count = await crawler.count(result['word'], result['urls'])
        resp = {'success': True}
        resp.update({"urls": [count]})
        return jsonify(resp)
