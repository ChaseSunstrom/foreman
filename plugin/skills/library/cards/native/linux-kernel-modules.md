---
name: linux-kernel-modules
title: Linux Kernel Modules
area: native
tags: [linux, kernel, module, kbuild, driver, c, kasan]
detect: [file:Kbuild, file:Kconfig, file:*.mod.c, file:modules.order]
related: [embedded-c, sanitizers, ebpf, io-uring, valgrind]
---
Out-of-tree Linux kernel modules: Kbuild, init/exit and error unwinding, user-copy safety, locking, and KASAN/lockdep checks in a VM.

## Verify
- `make -C /lib/modules/$(uname -r)/build M=$PWD modules`: build against the running kernel's headers.
- `modinfo ./mymod.ko`: metadata (license, vermagic, parameters) is correct.
- `make -C /lib/modules/$(uname -r)/build M=$PWD C=2 CF="-D__CHECK_ENDIAN__" modules`: sparse static checks, if sparse is installed.
- `scripts/checkpatch.pl --no-tree -f mymod.c`: kernel style, from a kernel source tree.
- `sudo insmod ./mymod.ko && sudo dmesg | tail && sudo rmmod mymod`: load, observe, unload cleanly (run in a VM, never on a machine you cannot reboot).

## Test first
Test in a VM against a kernel with `CONFIG_KASAN`, `CONFIG_LOCKDEP` and `CONFIG_DEBUG_ATOMIC_SLEEP`. Write the user-space test that exercises the interface first and watch it fail.
```c
// tests/test_dev.c
int fd = open("/dev/mydev", O_RDWR);
assert(fd >= 0);
char buf[4];
assert(write(fd, "ab", 2) == 2);
assert(read(fd, buf, 2) == 2 && memcmp(buf, "ab", 2) == 0);
assert(write(fd, NULL, 1) == -1 && errno == EFAULT);   // bad user pointer must not oops
```
Also load, unload and reload the module in a loop to catch leaks.

## Do
- Keep a minimal `Kbuild` (`obj-m += mymod.o`; multi-file: `mymod-y := a.o b.o`) and a Makefile that calls `$(MAKE) -C $(KDIR) M=$(PWD) modules`.
- Add `MODULE_LICENSE("GPL")`, `MODULE_AUTHOR`, and `MODULE_DESCRIPTION`; without a GPL license, GPL-only symbols fail to resolve.
- In `init`, acquire resources in order and on failure unwind with `goto err_label` in reverse order; `exit` mirrors it exactly. Prefer `devm_*` resource APIs in drivers.
- Move data across the boundary only with `copy_from_user`, `copy_to_user`, `get_user`, `put_user`; check the return value and return `-EFAULT`.
- Use `kzalloc(GFP_KERNEL)` in process context and `GFP_ATOMIC` only where sleeping is illegal; check for NULL.
- Protect shared state with a mutex (sleepable) or a spinlock (atomic context); do not sleep while holding a spinlock.
- Return negative errno values (`-EINVAL`, `-ENOMEM`), not -1.
- Log with `pr_info`/`dev_err`, and rate-limit hot paths with `dev_err_ratelimited`.

## Avoid
- Dereferencing user pointers directly: oops or a security hole. Use the copy helpers.
- Sleeping in interrupt, softirq or spinlock context (`kmalloc(GFP_KERNEL)`, `mutex_lock`): "scheduling while atomic". Use `GFP_ATOMIC` or defer to a workqueue.
- Forgetting to cancel timers, work items and free IRQs in `exit`: use-after-free after `rmmod`. Call `del_timer_sync`, `cancel_work_sync`, `free_irq`.
- Leaving error-path leaks by early `return`: use the single unwind path.
- Using floating point, large stack arrays (stack is small, a few KiB-16 KiB): use `kmalloc`.
- Building against mismatched headers: vermagic mismatch on load. Use the headers of the target kernel.
- `printk` without a level or in tight loops: floods the log.

## Review
- [ ] All user-space memory access goes through copy helpers with checked returns.
- [ ] Allocation flags match the context; no sleeping under spinlocks.
- [ ] Init failure unwinding and exit release exactly what was acquired.
- [ ] A load, use and unload loop is clean under KASAN and lockdep.
- [ ] Errors are negative errno values; logs are leveled and rate-limited.
