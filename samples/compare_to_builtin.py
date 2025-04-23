import mimetypes

import content_types


def main():
    print('Compare types in mimetypes vs content-types.')
    in_mime_only = set()
    differ = set()
    for k, v in mimetypes.types_map.items():
        cv_v = content_types.EXTENSION_TO_CONTENT_TYPE.get(k.lower().strip('.'))
        if not cv_v:
            in_mime_only.add((k, v))
            continue

        if cv_v != v:
            differ.add(((k, v), (k, cv_v)))
            continue

    only_ct = set()
    for k, v in content_types.EXTENSION_TO_CONTENT_TYPE.items():
        mv = mimetypes.types_map.get('.' + k)
        if not mv:
            only_ct.add((k, v))
            continue

    print(f'There are {len(differ):,} types where mimetypes and content-types disagree')
    for (mk, mv), (ct_k, ct_v) in sorted(differ):
        print(f'mimetypes: {mk} {mv}, content-types: {ct_k} {ct_v}')
    print()

    print(f'There are {len(in_mime_only):,} types in mimetypes that are not in content-types')
    for k, v in sorted(in_mime_only):
        print(f'{k.ljust(5)}: {v}')
    print()

    print(f'There are {len(only_ct):,} types in content-types that are not in mimetypes')
    for k, v in sorted(only_ct):
        print(f'.{k.ljust(5)} -> {v}')
    print()


if __name__ == '__main__':
    main()
