# smsapi
Implementation of a python flask based REST API for inbound and outbound sms


### Local deployment (ENV=dev)
---

**Requirements:**<br/>
```
  1. postgresql == 9.5.2
  2. redis server == 3.0.7
  3. Python == 2.7
  4. setuptools == 28.6.1
```
<br/>
To run the project locally, follow the below steps: <br/>
1. Clone the repository - `git clone https://github.com/akshay58538/smsapi.git`
2. Replace your redis and postgre urls in `plivo/sms/config/config_dev.json`
3. Install the package by running - `sudo python setup.py install`
4. Start the gunicorn server by running `gunicorn plivo.sms.app:app --log-file - -b 0.0.0.0 --log-level info --access-logfile -`
5. The server will now be accessible at [http://localhost:8000](http://localhost:8000)

<br/>
To run the API functional __tests__: <br/>
1. Follow steps 1-3 above
2. Run the tests - `python tests/plivo/sms/test_resource.py`

**Note**: tests are executed in `dev` environment and use the dev config - access the postgre and redis specified

There was some issue while trying to run the tests with nose, as such the command `sudo python setup.py nosetests` doesnt yet work.