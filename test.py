import libusb_package_tng
import usb.backend.libusb1
import usb.core
import sys


be = usb.backend.libusb1.get_backend(
        find_library=libusb_package_tng.find_library)
if be is None:
    print('No compatible library in libusb_package_tng.')
    print('Trying OS library...')
    be = usb.backend.libusb1.get_backend()
    if be is None:
        print('No OS library available.')
        sys.exit(-1)
    print('Found compatible OS library.')
else:
    print('Found compatible library in libusb_package_tng.')


print(list(usb.core.find(find_all=True, backend=be)))
