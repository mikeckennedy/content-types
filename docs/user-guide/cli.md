# Command line

The package ships a `content-types` console script for one-off lookups from the shell. This page covers installing it, its flags, and its exit codes.


# Install

The package installs a `content-types` console script. For machine-wide use, install it as a tool.

``` bash
uv tool install content-types
# or
pipx install content-types
```

Inside a project that already depends on the package, the script is on the virtualenv's path, so `uv run content-types ...` also works.


# Use

The script takes one argument, a filename or extension, and prints the content type. It does the forward lookup only; there is no reverse lookup on the command line.

``` bash
content-types example.jpg
# image/jpeg

content-types .webp
# image/webp

content-types data.parquet
# application/vnd.apache.parquet
```

The argument goes through [get_content_type()](../reference/get_content_type.md#content_types.get_content_type) with its defaults, so an unknown extension prints `application/octet-stream` and still exits with status 0. Extra arguments after the first are ignored.


# Flags and exit codes

| Invocation | Output | Exit code |
|----|----|----|
| `content-types NAME` | the content type, or `application/octet-stream` for an unknown extension | 0 |
| `content-types` | usage text on stdout | 1 |
| `content-types -h` or `--help` | usage text | 0 |
| `content-types --version` | the installed package version | 0 |

There are no environment variables and no configuration file. The script is the function `content_types.cli()` wired up in `pyproject.toml`, so you can also run it as `python -m` style code by calling that function.
