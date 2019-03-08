## Installation

`pip install decaptcher`

## Usage

### Twocaptcha Backend Example

Service website is https://2captcha.com?from=3019071

```python
from decaptcher import Service

solver = Service('twocaptcha', api_key='2captcha.com API HERE')
print(solver.process_file('captcha.png'))
```


### Rucaptcha Backend Example

Service website is https://rucaptcha.com?from=3019071

```python
from decaptcher import Service

solver = Service('rucaptcha', api_key='RUCAPTCHA_KEY')
print(solver.process_file('captcha.png'))
```


### Antigate Backend Example

Service website is http://getcaptchasolution.com/ijykrofoxz

```python
from decaptcher import Service

solver = Service('antigate', api_key='ANTIGATE_KEY')
print(solver.process_file('captcha.png'))
```


### Browser Backend Example

Browser backend just displays captcha in default browser and wait you enter solution in console.

```python
from decaptcher import Service

solver = Service('browser')
print(solver.process_file('captcha.png'))
```
