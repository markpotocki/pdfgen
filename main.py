import json
import sheetsapi
import vouchergen
import time

def main():
    load_config()
    filter_values = sheetsapi.retrieve_spreadsheet_data()
    print(filter_values)
    for val in filter_values:

        vouchergen.write_pdf('output/%s-%s.pdf' % (val[0], time.time()),  val[1])


def load_config():
    with open('config.json') as config:
        config_dict = json.load(config)
        sheetsapi.init_config(config_dict['sheetsapi'])


if __name__ == '__main__':
    main()
