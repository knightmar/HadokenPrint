import usb.core

usbs = []


def detect_new_usb():
    dev = usb.core.find(find_all=True)
    try:
        for e in dev:
            print(e.product)
    except ValueError as e:
        print(e)


detect_new_usb()
