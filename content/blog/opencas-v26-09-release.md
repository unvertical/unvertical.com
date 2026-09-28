---
title: "OpenCAS v26.09 Released"
date: 2026-09-29
draft: false
tags: ["opencas", "release"]
description: "Prefetching, in-flight upgrade, DKMS packaging for RPM and DEB, netlink interface, and support for Linux 7.2."
cta_title: "Running OpenCAS in production?"
cta_text: "If you want help planning the upgrade, trying the new features, or you'd like to ask any other question, get in touch. In return, we'd love to learn about your setup and hear your feedback."
---

We're happy to announce that **OpenCAS v26.09** is out. It collects six months of work since v26.03, while the v26.03.x line kept receiving fixes and updates in four patch releases. This release adds a new prefetch subsystem, a first step toward upgrading OpenCAS without taking cached devices offline, a DKMS option for RPM packages, and support for Linux kernels up to 7.2. It also lays a foundation for integrations with telemetry systems.

## Highlights

### Prefetching with readahead

OpenCAS can now fetch data into the cache *before* your application asks for it. The new prefetch subsystem in the Open CAS Framework (OCF) ships with a first policy, **readahead**: when OpenCAS sees a sequential read stream, it pulls the following data into cache ahead of time.

Prefetching is disabled by default. You can enable it per cache:

```bash
casadm --set-param --name prefetch --cache-id 1 --policy readahead
casadm --set-param --name prefetch-readahead --cache-id 1 --threshold 512
```

The threshold sets how many bytes (in KiB) a sequential stream must reach before prefetching starts. Prefetched I/O gets its own I/O class, so you can see how much it contributes in the statistics.

### In-flight upgrade with cache disconnect/connect

Upgrading OpenCAS used to mean stopping caches and taking the cached devices offline. v26.09 introduces **cache disconnect/connect**, the groundwork for upgrading OpenCAS while the cached block devices stay in place.

Block device management now lives in a new kernel module, `cas_bd`. When a cache is disconnected, its exported devices (`/dev/casX-Y`) are handed over to `cas_bd`, which keeps them present in either pass-through or frozen mode. With all caches disconnected, the `cas_cache` module can be unloaded and replaced with a newer version, and the caches can then be connected again.

On top of these changes we also introduced a special build mode producing the `cas_cache` module in two versions, compatible with old and new `cas_bd` symbol versions. That allows for smooth transition before `cas_bd` gets reloaded in a new version (which would typically happen on the next reboot). 

When built in `FALLBACK_SYMVERS` mode, OpenCAS can be upgraded using a new `make upgrade` target, which takes care of installing all the new files, modules in both versions, and loading the right combination for the cache to be properly loaded or connected.

This is a first step, and it has limits. The upgrade procedure is not fully automated yet (`make upgrade` does not take care of disconnecting the caches and handling all the related rollback scenarios), and it only works between versions with compatible cache metadata, because there is no metadata migration yet. We're shipping it now as a useful developer tool, as we continue working to make it more complete in future releases.

If you are interested in trying it, these are the commands:

```bash
# In the source tree of the new version
./configure
make FALLBACK_SYMVERS=/lib/modules/$(uname -r)/extra/block/opencas/cas_bd.symvers

# Disconnect the cache (repeat for every running cache)
casadm --script --disconnect-cache --cache-id 1

# Install the new version and load the new cas_cache
make upgrade

# Connect the cache again
casadm --script --connect-cache --cache-device /dev/nvme0n1
```

By default, the exported devices are frozen while the cache is disconnected, so I/O waits until the cache is connected again. On connect the cache metadata is loaded. With `--pass-through`, I/O goes straight to the backend devices in the meantime, which is similar to cache detach, and on the following connect the cache starts empty.

With `--no-flush`, dirty data is not flushed on disconnect, which means the connect will also load the dirty data, but in case anything goes wrong during the upgrade, you risk data loss. You can't combine `--no-flush` with `--pass-through`, because in `--no-flush` mode the data on the backend devices is not synced.

### DKMS packaging for RPM and DEB

RPM packages now have an option to ship the kernel modules as DKMS source, which is built on the target machine. It does not replace the packaging method we used so far - the prebuilt kernel module packages are still available, and you can choose the one that fits your setup.

The two variants are mutually exclusive, and you can switch between them in both directions. Installing the DKMS package migrates an existing prebuilt install to DKMS, and installing the prebuilt package migrates it back.

Both RPM and DEB packages are now covered by automated tests. They got less attention than they deserved so far, so in this release we fixed a number of issues and polished them.

Thanks to our community contributors for their work on DKMS support.

### Linux kernel 7.2 support

OpenCAS v26.09 builds and runs on Linux kernels up to 7.2. This covers distributions that adopted the freshest kernel versions, including Ubuntu 26.04 LTS and Proxmox VE 9.2 (kernel 7.0), Fedora 44 (kernel 7.1), openSUSE Tumbleweed (kernel 7.2), and the upcoming Fedora 45 (kernel 7.2).

## Other improvements

- **Cleaner statistics:** `casadm` now shows statistics for the background cleaner.
- **Packaging:** installation, upgrade and uninstall of the packages got several fixes, and building from source is more reliable.
- **Fixes:** this release includes a number of bug fixes, among others for better handling of cache device failures and improved stability under intensive workload.
- **Testing:** we added a number of new tests, both for the new features and for the existing ones.

## Experimental features

This release also includes several features that are **disabled by default** and not yet ready for production use:

- **netlink interface** for querying cache state frequently without disturbing its operation, required for telemetry system integration,
- **libopencas** userspace library, a wrapper for the netlink interface,
- **Prometheus exporter** for OpenCAS metrics, built on top of libopencas, together with a sample Grafana dashboard.

We consider them unstable and they still lack proper test coverage.

To try them, build OpenCAS from source with `./configure --with-netlink`. They are not included in the packages yet. We'd welcome feedback from anyone who tries them.

## Getting v26.09

You can get the source and full changelog from the [v26.09 release page on GitHub](https://github.com/Open-CAS/open-cas-linux/releases/tag/v26.09).

If you're interested in official, tested and supported packages, they're available as part of our [subscription plans](/#pricing).
