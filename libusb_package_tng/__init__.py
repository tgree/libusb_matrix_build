import importlib.resources
import platform
import sys


ARCH = platform.machine().lower()
LIBUSB_VERS = '1.0.29'


class NoSuchLibraryException(Exception):
    pass


def get_library_resource():
    '''
    Finds the libusb library that we would use for the current platform.
    '''
    # macOS
    if sys.platform == 'darwin':
        # macOS.
        release, _, machine = platform.mac_ver()
        major, minor = release.split('.')[:2]
        major, minor = int(major), int(minor)
        if major < 10:
            raise NoSuchLibraryException('No macOS library for ancient macOS.')

        if major >= 11:
            if machine == 'arm64':
                return 'libusb-macos-11.0-arm64-' + LIBUSB_VERS + '.dylib'
            return 'libusb-macos-11.0-x86_64-' + LIBUSB_VERS + '.dylib'

        assert machine != 'arm64'
        if minor >= 15:
            return 'libusb-macos-10.15-x86_64-' + LIBUSB_VERS + '.dylib'
        if minor >= 13:
            return 'libusb-macos-10.13-x86_64-' + LIBUSB_VERS + '.dylib'
        if minor >= 9:
            return 'libusb-macos-10.9-x86_64-' + LIBUSB_VERS + '.dylib'

        raise NoSuchLibraryException('No macOS library for ancient macOS 10.')

    # Windows
    if sys.platform in ('cygwin', 'win32'):
        # Windows.
        if sys.maxsize > 2**32:
            return 'libusb-ms64-' + LIBUSB_VERS +'.dll'
        return 'libusb-ms32-' + LIBUSB_VERS + '.dll'

    # Linux otherwise.
    if 'arm64' in ARCH or 'aarch64' in ARCH:
        return 'libusb-linux-arm64-' + LIBUSB_VERS + '.so'
    if 'armv7l' in ARCH:
        lib, _ = platform.libc_ver()
        if 'musl' in lib.lower():
            return 'libusb-musl-armv7l-' + LIBUSB_VERS + '.so'
        return 'libusb-debian-10-armv7l-' + LIBUSB_VERS + '.so'
    if 'x86_64' in ARCH or 'amd64' in ARCH:
        return 'libusb-linux-x86_64-' + LIBUSB_VERS + '.so'
    if '386' in ARCH or '686' in ARCH:
        return 'libusb-linux-i686-' + LIBUSB_VERS + '.so'

    # Can't find one.
    raise NoSuchLibraryException(
        'No Linux libusb_package_2 library for ARCH %s' % ARCH)


def find_library(candidate):
    '''
    Look for a package resource matching the name.
    '''
    if candidate.startswith('libusb-1.0'):
        try:
            lib_name = get_library_resource()
            with importlib.resources.path('libusb_package_tng.libraries',
                                          lib_name) as p:
                path = p

            return str(path)
        except NoSuchLibraryException as e:
            print('Exception: %s' % repr(e))

    return None
