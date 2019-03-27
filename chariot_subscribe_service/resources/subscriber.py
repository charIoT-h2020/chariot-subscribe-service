import json
import falcon
import logging

from chariot_base.utilities import Traceable


# -*- coding: utf-8 -*-


class SubscriberResource(Traceable):
    def __init__(self, db):
        super(Traceable, self).__init__()
        self.tracer = None
        self.db = db
        self.subscribers = {
            'bms': {
                'sensors': [
                    'device_52806c75c3fd_Sensor04'
                ]
            }
        }

    def on_get(self, req, resp, id=None):
        if id is None:
           resp.json = self.subscribers
        else:
            id = id.lower()
            resp.json = self.subscribers[id]

    def on_post(self, req, resp):
        subscriber_id = req.get_json('id')
        sensor_id = req.get_json('sensor_id')

        rule = self.dispatcher.subscribers[subscriber_id]
        rule.sensors.add(sensor_id)

        resp.json = rule.dict()
