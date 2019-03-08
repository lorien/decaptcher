## Installation

Use command:

```shell
pip install -e git://github.com/lorien/decaptcher#egg=decaptcher
```

## Usage

### Twocaptcha Backend Example

Service website is https://2captcha.com?from=3019071

```python
from decaptcher import Service

solver = Service('twocaptcha', api_key='2captcha.com API HERE')
print(solver.process_file('captcha.png'))
# or
with open('captcha.png') as inp:
    print(solver.process(inp.read()))
# or
with open('captcha.png') as inp:
    print(solver.process(inp))
# You can pass extra parameters (described in 2captcha documentation)
# using task_options arguments:
print(solver.process_file('captcha.png', task_options={
    'regsense': 1,
    'min_len': 4,
}))

```

### Solving custom captcha type using 2captcha.com

Decaptcher library supports any custom captcha supported by 2captcha.com service.
Just use `task_options` argument to pass all required parameters. 
For example, to solve text captcha do:
```python
from decaptcher import Service

solver = Service('twocaptcha', api_key='2captcha.com API HERE')
print(solver.process(task_options={
    'lang': 'en',
    'textcaptcha': 'Name of first day of week',
}))
```

### Getting captcha ID along the solution

To get catpcha ID pass `verbose=True` to `process` method:

```python
solver = Service('twocaptcha', api_key='2captcha.com API HERE')
print(solver.process_file('captcha.png', verbose=True))
````

You get result like:
```python
{"task_id": "captcha ID", "result": "captcha text"}
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
