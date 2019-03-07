import json
from decaptcher.service import Service


def main():
    with open('var/config.json') as inp:
        config = json.loads(inp.read())
    srv = Service('rucaptcha', api_key=config['rucaptcha_key'])
    res = srv.process_file('var/captcha.jpg')
    print(res)


if __name__ == '__main__':
    main()
