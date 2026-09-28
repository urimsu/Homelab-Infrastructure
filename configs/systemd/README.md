# systemd notes

No host-specific unit file is included because the service user, executable path, runtime, and privilege requirements are environment-dependent. For a local service, use a dedicated unprivileged account, explicit working directory, restricted filesystem access where practical, and environment files stored outside the repository with private permissions. Do not place tokens in a unit file committed to Git. Validate a unit with `systemd-analyze verify` on the target distribution before enabling it.
