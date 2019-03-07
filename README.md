## Installation

`pip install decaptcher`

## Usage

```
from decaptcher import Service
srv = Service('rucaptcha', api_key='...')
with open('captcha.jpg') as inp:
    raw_data = inp.read()
    res = srv.process_data(raw_data)
# OR just
res = srv.process_file('captcha.jpg')
print('Solution is %s' % res)
```
