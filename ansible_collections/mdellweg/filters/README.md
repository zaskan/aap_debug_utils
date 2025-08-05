# Filters

An Ansible collection of random filters I missed at some point.

## Examples
```
- name: Task that will be executed when conf_value is not empty
  debug:
    msg: "conf_value: {{ conf_value }}"
  when: conf_value is not mdellweg.filters.empty

- name: Use jq syntax to traverse structured data
  debug:
    msg: "{{ conf_dict | mdellweg.filters.jq('.key1[]') }}"

- name: Writing python values
  lineinfile:
    dest: settings.py
    line: "CONSTANT = {{ conf_dict.key2 | mdellweg.filters.repr }}"

- name: Check expected version
  assert:
    that:
      - reported_version | mdellweg.filters.canonical_semver == (expected_version | mdellweg.filters.canonical_semver)
```
