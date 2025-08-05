# Copyright (c) 2020 Matthias Dellweg
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

try:
    import jq

    HAS_JQ = True
except ImportError:
    HAS_JQ = False

try:
    from packaging.version import parse as parse_version

    HAS_PACKAGING = True
except ImportError:
    HAS_PACKAGING = False

from ansible.module_utils import six
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils._text import to_native, to_text
from ansible.errors import AnsibleError


__metaclass__ = type


def jq_filter(value, filter_expression, all=False):
    """
    Parse input with jq language.
    """
    if not HAS_JQ:
        raise AnsibleError(missing_required_lib("jq"))
    if all:
        return jq.all(filter_expression, value)
    else:
        return jq.first(filter_expression, value)


def map_to_native(value):
    if isinstance(value, six.string_types):
        return to_native(value)
    if isinstance(value, dict):
        return {map_to_native(key): map_to_native(val) for key, val in value.items()}
    if isinstance(value, list):
        return [map_to_native(val) for val in value]
    return value


def repr_filter(value):
    """
    Convert value into python representation string.
    """
    return to_text(repr(map_to_native(value)))


def canonical_semver_filter(value):
    """
    Represent a semantic version in a canonical form.
    """
    return to_text(str(parse_version(to_native(value))))


class FilterModule(object):
    def filters(self):
        return {
            "canonical_semver": canonical_semver_filter,
            "jq": jq_filter,
            "repr": repr_filter,
        }
