# python-securedrop-api

Experimental SDK for the [SecureDrop](https://seucredrop.org) API.

## STOP! WARNING! PRE-ALPHA

This is for being developed to test an in-progress branch in the main SecureDrop repo. This API is
neither deployed nor stable.

THIS SHOULD NOT BE USED ANYWHERE FOR ANY REASON.

## Development

Requires:

```
pip install tox tox-pyenv
for v in 3.4.8 3.5.5 3.6.6 3.7.0; do
  pyenv install $v
done
```

## License

This work is dual licensed under the MIT and Apache-2.0 licenses. See [LICENSE-MIT](./LICENSE-MIT)
and [LICENSE-APACHE](./LICENSE-APACHE) for details.
