import json

import price


def load_orders(text):
    return json.loads(text, object_hook=lambda d: {**d, "gross": price.with_vat(d["net"])} if "net" in d else d)


if __name__ == "__main__":
    print(load_orders('[{"net": 10}]'))
