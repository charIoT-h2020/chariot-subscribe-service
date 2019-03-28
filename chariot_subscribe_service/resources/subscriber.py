import json
import falcon
import logging
from bson.json_util import dumps, RELAXED_JSON_OPTIONS

from chariot_base.utilities import Traceable


# -*- coding: utf-8 -*-


class SubscriberResource(Traceable):
    def __init__(self, db):
        super(Traceable, self).__init__()
        self.tracer = None
        self.db = db

    def on_get(self, req, resp, id=None):
        span = self.start_span_from_request('get_subscriber', req)
        if id is None:
            result = self.db.subscribers.find()
        else:
            self.set_tag(span, 'id', id)
            result = self.db.subscribers.find_one({'id': id.lower()})

        resp.body = dumps(result, json_options=RELAXED_JSON_OPTIONS)
        self.close_span(span)

    def on_post(self, req, resp):
        span = self.start_span_from_request('edit_subscriber', req)
        subscriber_id = req.get_json('subscriber_id').lower()
        sensor_id = req.get_json('sensor_id')

        subscriber = self.db.subscribers.find_one({'id': subscriber_id})
        if subscriber is None:
            self.set_tag(span, 'updated', False)
            subscriber = {
                'id': subscriber_id,
                'sensors': [
                    sensor_id
                ]
            }
            result = self.db.subscribers.save(subscriber)
        else:
            self.set_tag(span, 'updated', True)
            result = self.db.subscribers.update(subscriber, { "$addToSet": { "sensors": sensor_id } } )

        resp.body = dumps(result, json_options=RELAXED_JSON_OPTIONS)
        self.close_span(span)
