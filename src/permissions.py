import contextlib
import os
import stat


@contextlib.contextmanager
def user_owned_outputs(paths):
    owner = None

    if os.geteuid() == 0 and 'SUDO_UID' in os.environ and 'SUDO_GID' in os.environ:
        owner = (int(os.environ['SUDO_UID']), int(os.environ['SUDO_GID']))

        if min(owner) < 0:
            raise ValueError('invalid sudo user or group ID')

    parents = set()

    for path in paths:
        for parent in path.parents:
            if parent.exists():
                break

            parents.add(parent)

    try:
        yield
    finally:
        if owner is not None:
            outputs = set(paths) | parents

            for path in paths:
                if path.is_dir() and not path.is_symlink():
                    outputs.update(path.rglob('*'))

            for path in outputs:
                # leave symlink targets and unrelated existing directories alone
                if path.is_symlink() or not path.exists():
                    continue

                mode = path.stat().st_mode
                access = stat.S_IRUSR | stat.S_IWUSR

                if stat.S_ISDIR(mode):
                    access |= stat.S_IXUSR

                os.chown(path, *owner)
                path.chmod(stat.S_IMODE(mode) | access)
