libusb_package_tng
==================
This package embeds the libusb library for use with pyusb so that the user
doesn't need to install it manually (which might require Homebrew on macOS or
more difficult measures on Windows).  It is inspired by the libusb_package
package, but uses a different approach.

libusb_package requires that the package be updated for every minor Python
release due to how it levereages cibuildwheel to build everything.  That
strategy doesn't make much sense because the underlying libusb library doesn't
change at all when a new Python is released.  In fact, the underlying libusb
library is typically built against very old versions of the target OS so that
it can be dynamically loaded in all circumstances so you normally don't even
need to rebuild libusb for a new version of your OS - the only time it makes
sense to rebuild libusb is if the libusb project itself releases a new version
of the library.

libusb_package_tng instead uses a strategy where we package up versions of
libusb that target all the major OS distributions, going reasonably far back
in time.  On macOS, GitHub build actions are used to build binaries that should
work on macOS 10.9, 10.13, 10.15 and then one version that runs on 11.0 and
later.  On Windows, we use the binaries released by the libusb project that
are built against VS2019.  For Linux, we have a set of Docker files that can be
used to build Docker images that build libusb directly for a number of
different platforms, including x86_64, i686, arm64 and armv7l binaries.  The
x86_64, arm64 and i686 binaries are built against manylinux2014 and so should
work on any distribution with glibc 2.17 or higher.  The armv7l binaries are
built against Debian 10 for Raspberry Pi support (they will not work on older
versions of Raspbian) and against musllinux_1_2 for any musllinux clients.

libusb_package_tng has been tested on Raspbian 10 (armv7l), on fairly recent
versions of macOS (both ARM and x86) and on fairly recent versions of Linux
(Ubuntu 22+, only x86).  Neither the musllinux armv7l nor i686 builds have been
tested since I don't have access to suitable hardware and older versions of
Linux have not been tested at all.  It has also been tested on Windows 11 build
22631, 64-bit x86.  It isn't immediately clear if the Windows .dlls provided by
the libusb project include ARM support.


Installing
==========
The easiest way to install is via pip::

    python3 -m pip install libusb_package_tng

You can also install from a copy of the repository using 'make install' on a
macOS or Linux system.


API
===
The main purpose of libusb_package_tng is to provide the find_library() API
required by pyusb.  We embed the various libusb builds directly in our package
and pass the correct one out as the result of find_library().  Here is a sample
script to use libusb_package_tng to provide the back-end for pyusb::

    import usb.backend.libusb1
    import usb.core
    import libusb_package_tng

    be = usb.backend.libusb1.get_backend(
            find_library=libusb_package_tng.find_library)
    assert be is not None
    print(list(usb.core.find(find_all=True, backend=be)))

If you want to fall back to checking for an OS copy of libusb in the event that
libusb_package_tng doesn't have a version that works on your system, you could
do the following instead::

    be = usb.backend.libusb1.get_backend(
            find_library=libusb_package_tng.find_library)
    if be is None:
        be = usb.backend.libusb1.get_backend()
    assert be is not None

The downside to this is that libusb_package_tng guarantees the version of the
libusb library that will be used, while the OS version could be something much
older.


Building
========
To build the macOS libraries, a commit needs to be submitted against the GitHub
repository to trigger the GitHub action that builds the macOS ARM and x86
matrices.  The yaml files that describe these are under .github/workflows/.
The build artifacts are then downloaded from the completed workflow run and 
manually copied into place.

To build the Linux libraries, you'll need to have Docker installed.  Simply
execute the make_linux_libraries.sh script and it will pull all the images and
build as appropriate.  The build products will be stripped and copied directly
into place.  These Docker images have been tested on an M1 MacBook Pro on macOS
15.7 using Orbstack but should in theory work elsewhere.  QEMU and/or Rosetta
are used transparently and I'm not sure if that is a feature or Orbstack or of
Docker itself, but it works great to build the Linux matrix.  GitHub actions
are not appropriate for this because we want to target very old versions of
Linux to get the earliest glibc version possible.

The Windows libraries come pre-built from the libusb GitHub release files.  The
libusb-<version>.7z file in the official libusb release contains pre-built
Windows binaries; this archive is downloaded manually, extracted, and then the
VS2019 .dll versions are manually copied into place.


Versioning
==========
libusb_package_tng uses the same versioning scheme as libusb_package.  The
first three parts of the version number correspond to the version of libusb
that is embedded in our package; the fourth part of the version number is our
internal release number.  For instance, version 1.0.29.0 is the very first
release of libusb_package_tng and it embeds libusb 1.0.29.  Since it was
obviously not perfect on the first release, version 1.0.29.1 has since been
released to fix a few things.  The fourth number will continue to increment as
we make improvements to libusb_package_tng.  The libusb project has recently
released libusb version 1.0.30, so we will pull that in soon and reset our
release number back to 0.  I.e., the first libusb_package_tng release for
libusb 1.0.30 will be 1.0.30.0.


Thank You
=========
I would like to thank the maintainers of the libusb_package repository who have
worked over the years to provide updates.  Embedding libusb inside a Python
package is a great idea and really simplifies the workflow for end-users that
may want to talk to a USB device but don't want to mess with Windows drivers or
other back-ends.  As an employee of a company that builds USB devices, we have
found it to be an invaluable tool and hopefully libusb_package_tng will be as
useful to others while being easier to maintain.
