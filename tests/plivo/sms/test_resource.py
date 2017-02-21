import json
import unittest
from base64 import b64encode
from plivo.sms.app import app
from plivo.sms.config.provider import ConfigProvider


class SmsInboundTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        # Fake redis and postgre here

    def tearDown(self):
        pass
        # Clear redis and postgre here

    def test_inbound_405(self):
        response = self.app.get('/sms/inbound')
        self.assertEqual(response.status_code, 405)
        response_body = json.loads(response.data)
        self.assertTrue(response_body.get('error'))

    def test_outbound_405(self):
        response = self.app.get('/sms/outbound')
        self.assertEqual(response.status_code, 405)
        response_body = json.loads(response.data)
        self.assertTrue(response_body.get('error'))

    def test_inbound_403(self):
        response = self.app.post('/sms/inbound', data=json.dumps({
            'to': '4924195509049',
            'from': '4924195509012',
            'text': 'Test text 1'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response_body = json.loads(response.data)
        self.assertTrue(response_body.get('error'))
        self.assertEqual(response_body.get('error'), "Unauthorized Access")

    def test_outbound_403(self):
        response = self.app.post('/sms/outbound', data=json.dumps({
            'to': '4924195509049',
            'from': '4924195509012',
            'text': 'Test text 1'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response_body = json.loads(response.data)
        self.assertTrue(response_body.get('error'))
        self.assertEqual(response_body.get('error'), "Unauthorized Access")

    def test_inbound_403_invalid_user(self):
        user_and_pass = b64encode(b"plivo2:20S0KPNOIM").decode("ascii")
        response = self.app.post('/sms/inbound', data=json.dumps({
            'to': '4924195509049',
            'from': '4924195509012',
            'text': 'Test text 1'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response.status_code, 403)
        response_body = json.loads(response.data)
        self.assertTrue(response_body.get('error'))
        self.assertEqual(response_body.get('error'), "Unauthorized Access")

    def test_outbound_403_invalid_user(self):
        user_and_pass = b64encode(b"plivo2:20S0KPNOIM").decode("ascii")
        response = self.app.post('/sms/inbound', data=json.dumps({
            'to': '4924195509049',
            'from': '4924195509012',
            'text': 'Test text 1'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response.status_code, 403)
        response_body = json.loads(response.data)
        self.assertTrue(response_body.get('error'))
        self.assertEqual(response_body.get('error'), "Unauthorized Access")

    def test_inbound_400_invalid_to(self):
        user_and_pass = b64encode(b"plivo1:20S0KPNOIM").decode("ascii")
        response = self.app.post('/sms/inbound', data=json.dumps({
            'to': '61881666926',
            'from': '4924195509012',
            'text': 'Test text 1'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.data)
        self.assertTrue(response_body.get('error'))
        self.assertEqual(response_body.get('error'), "to parameter not found")

    def test_outbound_400_invalid_from(self):
        user_and_pass = b64encode(b"plivo1:20S0KPNOIM").decode("ascii")
        response = self.app.post('/sms/outbound', data=json.dumps({
            'to': '61881666926',
            'from': '61871112920',
            'text': 'Test text 1'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response.status_code, 400)
        response_body = json.loads(response.data)
        self.assertTrue(response_body.get('error'))
        self.assertEqual(response_body.get('error'), "from parameter not found")

    def test_message_sending_blocked_stop(self):
        from_number = '4924195509012'
        to_number = '4924195509193'
        user_and_pass = b64encode(b"plivo1:20S0KPNOIM").decode("ascii")
        response_inbound = self.app.post('/sms/inbound', data=json.dumps({
            'to': to_number,
            'from': from_number,
            'text': 'STOP'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response_inbound.status_code, 200)
        response_body = json.loads(response_inbound.data)
        self.assertFalse(response_body.get('error'))
        self.assertTrue(response_body.get('message'))
        self.assertEqual(response_body.get('message'), "inbound sms ok")

        response_outbound = self.app.post('/sms/outbound', data=json.dumps({
            'to': to_number,
            'from': from_number,
            'text': 'Test text 2'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response_outbound.status_code, 422)
        response_body = json.loads(response_outbound.data)
        self.assertTrue(response_body.get('error'))
        self.assertFalse(response_body.get('message'))
        self.assertEqual(response_body.get('error'), "sms from {0} to {1} blocked by STOP request".format(from_number,
                                                                                                          to_number))

    def test_message_sending_blocked_stop_1(self):
        from_number = '4924195509193'
        to_number = '4924195509012'
        user_and_pass = b64encode(b"plivo1:20S0KPNOIM").decode("ascii")
        response_inbound = self.app.post('/sms/inbound', data=json.dumps({
            'to': to_number,
            'from': from_number,
            'text': 'STOP\n'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response_inbound.status_code, 200)
        response_body = json.loads(response_inbound.data)
        self.assertFalse(response_body.get('error'))
        self.assertTrue(response_body.get('message'))
        self.assertEqual(response_body.get('message'), "inbound sms ok")

        response_outbound = self.app.post('/sms/outbound', data=json.dumps({
            'to': to_number,
            'from': from_number,
            'text': 'Test text 2'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response_outbound.status_code, 422)
        response_body = json.loads(response_outbound.data)
        self.assertTrue(response_body.get('error'))
        self.assertFalse(response_body.get('message'))
        self.assertEqual(response_body.get('error'), "sms from {0} to {1} blocked by STOP request".format(from_number,
                                                                                                          to_number))

    def test_message_sending_blocked_stop_2(self):
        from_number = '61871112947'
        to_number = '61871112948'
        user_and_pass = b64encode(b"plivo4:YHWE3HDLPQ").decode("ascii")
        response_inbound = self.app.post('/sms/inbound', data=json.dumps({
            'to': to_number,
            'from': from_number,
            'text': 'STOP\r'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response_inbound.status_code, 200)
        response_body = json.loads(response_inbound.data)
        self.assertFalse(response_body.get('error'))
        self.assertTrue(response_body.get('message'))
        self.assertEqual(response_body.get('message'), "inbound sms ok")

        response_outbound = self.app.post('/sms/outbound', data=json.dumps({
            'to': to_number,
            'from': from_number,
            'text': 'Test text 2'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response_outbound.status_code, 422)
        response_body = json.loads(response_outbound.data)
        self.assertTrue(response_body.get('error'))
        self.assertFalse(response_body.get('message'))
        self.assertEqual(response_body.get('error'), "sms from {0} to {1} blocked by STOP request".format(from_number,
                                                                                                          to_number))

    def test_message_sending_blocked_stop_3(self):
        from_number = '441224980089'
        to_number = '441224459482'
        user_and_pass = b64encode(b"plivo2:54P2EOKQ47").decode("ascii")
        response_inbound = self.app.post('/sms/inbound', data=json.dumps({
            'to': to_number,
            'from': from_number,
            'text': 'STOP\r\n'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response_inbound.status_code, 200)
        response_body = json.loads(response_inbound.data)
        self.assertFalse(response_body.get('error'))
        self.assertTrue(response_body.get('message'))
        self.assertEqual(response_body.get('message'), "inbound sms ok")

        response_outbound = self.app.post('/sms/outbound', data=json.dumps({
            'to': to_number,
            'from': from_number,
            'text': 'Test text 2'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response_outbound.status_code, 422)
        response_body = json.loads(response_outbound.data)
        self.assertTrue(response_body.get('error'))
        self.assertFalse(response_body.get('message'))
        self.assertEqual(response_body.get('error'), "sms from {0} to {1} blocked by STOP request".format(from_number,
                                                                                                          to_number))

    def test_message_rate_limit_reached(self):
        from_number = '4924195509192'
        to_number = '3253280312'
        user_and_pass = b64encode(b"plivo1:20S0KPNOIM").decode("ascii")
        for i in range(ConfigProvider().getRequestCountThreshold()):
            response_outbound = self.app.post('/sms/outbound', data=json.dumps({
                'to': to_number,
                'from': from_number,
                'text': 'Test text ' + str(i)
            }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
            self.assertEqual(response_outbound.status_code, 200)
            response_body = json.loads(response_outbound.data)
            self.assertFalse(response_body.get('error'))
            self.assertTrue(response_body.get('message'))
            self.assertEqual(response_body.get('message'), "outbound sms ok")

        response_outbound = self.app.post('/sms/outbound', data=json.dumps({
            'to': to_number,
            'from': from_number,
            'text': 'Test text 51'
        }), content_type='application/json', headers={'Authorization': 'Basic %s' % user_and_pass})
        self.assertEqual(response_outbound.status_code, 429)
        response_body = json.loads(response_outbound.data)
        self.assertTrue(response_body.get('error'))
        self.assertFalse(response_body.get('message'))
        self.assertEqual(response_body.get('error'), "limit reached for from {}".format(from_number))

if __name__ == '__main__':
    unittest.main()
