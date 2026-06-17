# Plan: Add `guess_extension` / `guess_all_extensions` (reverse lookup) — issue #9

**Issue:** [#9 — Add method guess_extension](https://github.com/mikeckennedy/content-types/issues/9)
**Status:** Ready to implement (all §9 decisions resolved)
**Scope:** Add MIME-type → extension reverse lookup, mirroring (but improving on) stdlib `mimetypes`.

---

## 1. Goal

Today the library is one-directional: `get_content_type("file.pdf") → "application/pdf"`. Issue #9 asks
for the reverse, matching the stdlib `mimetypes` surface:

```python
import content_types

content_types.guess_extension("application/pdf")        # -> ".pdf"
content_types.guess_all_extensions("image/jpeg")        # -> [".jpg", ".jpeg", ".jpe"]
```

The commenter wants the full stdlib trio. Note `mimetypes.guess_type` is **already** covered by
`get_content_type`, so this plan adds only the two reverse functions: `guess_extension` and
`guess_all_extensions`.

## 2. Background — why this is "more work than the fallback one"

As Michael noted on the issue, the reverse direction is harder because the mapping is **many-to-one**.
Empirically measured against the current dict (and independently re-verified):

- **364** extensions map to **223** unique content types.
- **57** content types have **more than one** extension, so reversing must pick a *canonical* one.
- The two giant fallback buckets dominate: `text/plain` has **32** extensions, `application/octet-stream`
  has **24**.
- Examples of collision groups (in dict insertion order):
  - `image/jpeg` ← `jpg, jpeg, jpe`
  - `application/xml` ← `xml, xsl, rdf, wsdl, xpdl, nuspec`
  - `application/json` ← `json, map, babelrc, eslintrc, prettierrc`
  - `text/html` ← `htm, html`  ⚠️ (first-listed is the *less* canonical one)

**Key finding:** the dict is authored "canonical-first" within almost every group, so building the reverse
map by walking the forward dict and taking the **first** extension per type yields the correct canonical for
**53 of 57** groups and all 166 single-extension types. Only **4** groups need a correction (see §4).

## 3. Proposed public API

```python
def guess_extension(content_type: str, with_dot: bool = True) -> Optional[str]: ...
def guess_all_extensions(content_type: str, with_dot: bool = True) -> list[str]: ...
```

| Aspect | Behavior | Rationale |
|---|---|---|
| Return on hit | `guess_extension` → canonical ext; `guess_all_extensions` → all exts (canonical first) | — |
| Leading dot | Default **`.pdf`** (dotted). `with_dot=False` → `pdf` | stdlib + the issue example return dotted; dotted is what you concatenate onto a filename. `with_dot=False` serves dict-symmetry. |
| Unknown type | `guess_extension` → **`None`**; `guess_all_extensions` → **`[]`** | Matches stdlib exactly; reverse lookup legitimately has "no answer" (unlike `get_content_type`, which always has a sensible default). |
| `None` input | raises **`TypeError`** (message `'content_type cannot be None.'`) | Mirrors `get_content_type`'s existing `None` contract. |
| Empty / whitespace-only / param-only | → `None` / `[]` (a *miss*, not an error) | Matches `get_content_type` treating `''` as a normal non-raising miss. |
| Case | case-**insensitive** (lowercased) | MIME types are case-insensitive per RFC; matches stdlib. |
| MIME parameters | **stripped**: `'text/html; charset=utf-8'` → `.htm`/`.html` | **Deliberate divergence** — see §5. |
| `strict=` param | **omitted** | See §5. |
| Consistency | `guess_extension(t) == guess_all_extensions(t)[0]` always | Single source of canonical. |

Both functions are pure lookups into a reverse map that is **built lazily on first reverse call and cached**
thereafter — no per-call rescans, and importers who only ever use the forward direction (`get_content_type`
/ the shortcut constants) pay **zero** reverse-map construction cost. (The shortcut constants stay eager at
import, since they only need the forward dict.)

## 4. The canonical-extension strategy (the crux)

**Approach:** derive the reverse map from `EXTENSION_TO_CONTENT_TYPE` on first use (keeping it the single
source of truth — no second hand-maintained table that can drift), using **first-in-insertion-order** as the
canonical, then apply a **tiny 4-row override** for the groups where the first-listed extension is the
obscure/legacy alias.

| Content type | First-wins (wrong/legacy) | Canonical override | Why |
|---|---|---|---|
| `text/html` | `.htm` | **`.html`** | `.html` is the dominant modern form; `.htm` is a DOS 8.3 holdover. Matches stdlib. |
| `image/tiff` | `.tif` | **`.tiff`** | Full-name form matches the type; matches stdlib. |
| `video/mpeg` | `.mpg` | **`.mpeg`** | Full-name form matches the type; matches stdlib. |
| `application/x-msdownload` | `.dll` | **`.exe`** | `.exe` is the representative executable; a DLL is a special case. Matches stdlib. |

All four are *adjacent pairs* in the source dict, so an alternative is to simply reorder them in
`EXTENSION_TO_CONTENT_TYPE` (see §9, decision D). The plan recommends the **explicit override** because it
documents the canonical choice as a reviewable decision and is robust to future dict re-sorting.

**Important:** the override must promote the preferred extension to the **front** of the group's list, so
`guess_all_extensions("text/html") == [".html", ".htm"]` and the
`guess_extension(t) == guess_all_extensions(t)[0]` invariant holds.

**Groups deliberately NOT overridden** (first-wins is equal-or-better than stdlib's pick): `application/xml`
→ `.xml` (stdlib quirkily picks `.xsl`), `audio/midi` → `.midi`, `text/x-asm` → `.asm` (stdlib `.s`),
`application/x-troff` → `.roff`. Our choices are clearer/more modern by design.

**Fallback buckets:** no special-casing needed. First-wins already gives `application/octet-stream` →
`.bin` and `text/plain` → `.txt` (both match stdlib, and both coincide with `get_content_type`'s own
unknown-extension fallbacks, so the round-trip is naturally consistent). Specific aliases (`.pkl`, `.log`, …)
remain reachable via `guess_all_extensions`.

**Round-trip invariant — verified:** under this strategy, `get_content_type(guess_extension(t)) == t` holds
for **all 223** reversible content types (0 failures, confirmed by running it against the live dict).

## 5. Normalization & intentional divergences from stdlib

Normalize the input before lookup: `strip()` → drop everything after the first `;` → `strip()` again →
`lower()`. So `'  TEXT/HTML ; charset=utf-8 '` → `'text/html'`.

| Behavior | stdlib | This library | Verdict |
|---|---|---|---|
| Leading dot in output | dotted | dotted (default) | **match** |
| Unknown → `guess_extension` | `None` | `None` | **match** |
| Unknown → `guess_all_extensions` | `[]` | `[]` | **match** |
| Case-insensitive type | yes | yes | **match** |
| `None` input | raises `AttributeError` | raises `TypeError` | **diverge** (cleaner, mirrors `get_content_type`) |
| Whitespace in type | **not** stripped → `None` | stripped | **diverge** (forgiving) |
| MIME params (`; charset=…`) | **not** stripped → `None` | stripped | **diverge** (forgiving — HTTP `Content-Type` headers carry params; on-brand "more correct than stdlib") |
| `strict=` param | present (gates IANA vs common map) | **omitted** | **diverge** — the library has one curated table; `strict` would gate nothing and be a misleading no-op |
| `guess_all` list order | stdlib internal order | forward-dict insertion order, canonical-first | **diverge** — deterministic and more sensible (e.g. we lead `image/jpeg` with `.jpg`); do **not** claim byte-for-byte order parity with stdlib |

## 6. Implementation (single file: `content_types/__init__.py`)

`Optional` is already imported (line 4); add `import functools` (stdlib — not a packaged runtime dependency).
Add the helpers after `EXTENSION_TO_CONTENT_TYPE`, before `get_content_type`. Reference sketch:

```python
# Canonical-extension overrides for the few groups whose first-listed extension is the
# less-common alias. Promotes the preferred ext to the front of the reverse-map list so
# guess_extension() and guess_all_extensions()[0] always agree.
_CANONICAL_OVERRIDES: dict[str, str] = {
    'text/html': 'html',  # not 'htm'
    'image/tiff': 'tiff',  # not 'tif'
    'video/mpeg': 'mpeg',  # not 'mpg'
    'application/x-msdownload': 'exe',  # not 'dll'
}


@functools.cache
def _reverse_map() -> dict[str, list[str]]:
    """Reverse of EXTENSION_TO_CONTENT_TYPE: content type -> extensions (canonical first).

    Built lazily on first reverse lookup and cached for the process lifetime, so
    importers who only call get_content_type() never pay to construct it.
    """
    reverse: dict[str, list[str]] = {}
    for ext, content_type in EXTENSION_TO_CONTENT_TYPE.items():
        reverse.setdefault(content_type, []).append(ext)
    for content_type, preferred in _CANONICAL_OVERRIDES.items():
        exts = reverse.get(content_type)
        if exts and preferred in exts:
            exts.remove(preferred)
            exts.insert(0, preferred)
    return reverse


def _normalize_content_type(content_type: str) -> str:
    # 'text/html; charset=utf-8' -> 'text/html'
    content_type = content_type.strip()
    if ';' in content_type:
        content_type = content_type.split(';', 1)[0]
    return content_type.strip().lower()


def guess_extension(content_type: str, with_dot: bool = True) -> Optional[str]:
    if content_type is None:
        raise TypeError('content_type cannot be None.')
    exts = _reverse_map().get(_normalize_content_type(content_type))
    if not exts:
        return None
    return f'.{exts[0]}' if with_dot else exts[0]


def guess_all_extensions(content_type: str, with_dot: bool = True) -> list[str]:
    if content_type is None:
        raise TypeError('content_type cannot be None.')
    exts = _reverse_map().get(_normalize_content_type(content_type), [])
    return [f'.{e}' for e in exts] if with_dot else list(exts)
```

The reverse map is kept **private** (decision C, §9) — `_reverse_map()` is the only access point, used
internally by both functions. No public `CONTENT_TYPE_TO_EXTENSIONS` name and no PEP 562 `__getattr__` are
added, which keeps the module's public surface to just the two new functions.

Notes:
- **Laziness mechanism:** `@functools.cache` on a zero-arg builder is the concise idiom (thread-safe; a
  rare double-build under a race is harmless since the result is identical). A decorator-free equivalent is a
  module-level `_cache` sentinel populated on first call — pick whichever reads better in this flat module.
- `guess_all_extensions` returns a **copy** (`list(exts)` / new list comprehension) so callers can't mutate
  the cached map.
- Both functions stay well under ruff's max-complexity 10.
- Add full Google-style docstrings (Args/Returns/Raises/Example) matching `get_content_type`, each noting
  that returns are leading-dot, that unknown → `None`/`[]`, and that the canonical pick/order follow this
  library's table and may differ from stdlib.
- No new shortcut constants needed (those are content-type strings; reverse shortcuts aren't useful).

## 7. Tests (`tests/test_content_types.py`)

Match the existing class-based, spot + negative + invariant style. Three new classes:

**`TestGuessExtension`**
- `test_common_reverse_lookups` — `application/pdf`→`.pdf`, `image/png`→`.png`, `image/jpeg`→`.jpg`,
  `application/json`→`.json`, `audio/mpeg`→`.mp3`, `application/zip`→`.zip`, `text/markdown`→`.md`.
- `test_canonical_overrides` — **(corrected for the override)** `text/html`→`.html`, `image/tiff`→`.tiff`,
  `video/mpeg`→`.mpeg`, `application/x-msdownload`→`.exe`. Comment that these override the first-listed alias.
- `test_with_dot_false` — `guess_extension('application/pdf', with_dot=False) == 'pdf'`.
- `test_data_science_reverse_lookups` — `application/vnd.apache.parquet`→`.parquet`,
  `application/x-ipynb+json`→`.ipynb`, `application/yaml`→`.yaml`, `application/toml`→`.toml`,
  `application/vnd.sqlite3`→`.sqlite`.
- `test_unknown_type_returns_none` — `guess_extension('application/x-does-not-exist') is None`.
- `test_none_input_raises_typeerror` — `pytest.raises(TypeError)`.
- `test_empty_string_returns_none` — `''` and `'   '` → `None`.
- `test_case_insensitive` — `IMAGE/JPEG`→`.jpg`, `Application/PDF`→`.pdf`.
- `test_mime_parameters_are_stripped` — `'text/plain; charset=utf-8'`→`.txt`,
  `'application/json;charset=UTF-8'`→`.json`, `'text/html ; x=y'`→`.html`.
- `test_returns_leading_dot` — every non-`None` return `.startswith('.')`.

**`TestGuessAllExtensions`**
- `test_single_extension_type` — `application/pdf`→`['.pdf']` (a one-element list).
- `test_many_to_one_ordering_and_contents` — `image/jpeg`→`['.jpg', '.jpeg', '.jpe']`; first element equals
  `guess_extension('image/jpeg')`. Note order differs from stdlib's.
- `test_override_group_is_canonical_first` — `text/html`→`['.html', '.htm']`,
  `video/mpeg`→`['.mpeg', '.mpg', '.m1v', '.mpa', '.mpe', '.vob']`.
- `test_largest_collision_group` — `text/plain` returns 32 exts led by `.txt`; assert `result[0] == '.txt'`,
  `len(result) == 32`, `'.ini' in result`.
- `test_unknown_type_returns_empty_list` — `'made/up'`→`[]`, `''`→`[]`.
- `test_none_input_raises_typeerror`, `test_case_insensitive_and_param_stripping`,
  `test_with_dot_false`, `test_all_entries_are_dotted_and_unique`.

**`TestReverseLookupInvariants`** (property tests over the whole dict)
- `test_roundtrip_type_to_ext_to_type` — for every `t` in `set(EXTENSION_TO_CONTENT_TYPE.values())`:
  `guess_extension(t) is not None` **and** `get_content_type(guess_extension(t)) == t`. (Verified: 0 failures.)
- `test_guess_all_forward_consistency` — every `e` in `guess_all_extensions(t)` satisfies
  `get_content_type(e) == t`.
- `test_guess_extension_is_first_of_guess_all` — `guess_extension(t) == guess_all_extensions(t)[0]` for all `t`.
- `test_every_extension_is_reachable` — for every `ext` key, `('.' + ext) in
  guess_all_extensions(EXTENSION_TO_CONTENT_TYPE[ext])`.

The reverse map is private (decision C), so no public-dict test is needed; the invariants above already
exercise it thoroughly through the two functions.

Run: `uv run --with pytest pytest` (per CLAUDE.md). The existing suite is 35 tests; this adds ~22.

## 8. Docs, changelog, release

- **`README.md`** — in `## Usage`, after the forward examples, add a "Reverse lookup: MIME type → extension"
  block showing `guess_extension`/`guess_all_extensions`, the leading-dot returns, `None`/`[]` for unknowns,
  case-insensitivity, and param-stripping. One sentence: mirrors stdlib `mimetypes` but uses this library's
  larger/more-correct table (canonical pick can differ, e.g. it picks `.html` for `text/html`).
- **`change-log.md`** — under `## [Unreleased] → ### Added`, two entries referencing `(#9)` for the two
  functions (note case-insensitivity + param-stripping), plus a `Files:` line
  (`content_types/__init__.py`, `tests/test_content_types.py`, `README.md`).
- **Docstrings** — Google style, as in §6.
- **Docs site** — regenerate with `python scripts/build_docs.py` (Great Docs imports the live module, so the
  new docstrings flow into the API reference) and commit the regenerated `docs/`.
- **Release** — follow the existing flow (move `[Unreleased]` → `[X.Y.Z] - YYYY-MM-DD`, bump
  `pyproject.toml` version, tag `vX.Y.Z`). New public functions = a **minor** bump (e.g. `0.4.1` → `0.5.0`).

## 9. Decisions (resolved)

All four are settled; the plan above reflects them.

- **A. `with_dot` default → `True` (`.pdf`).** ✅ Dotted output by default, `with_dot=False` available.
- **B. MIME-parameter stripping → yes.** ✅ Strip `; charset=…` (and surrounding whitespace) before lookup;
  the one intentional, documented divergence from stdlib (stdlib returns `None` for parameterized input).
- **C. Public `CONTENT_TYPE_TO_EXTENSIONS` dict → no, keep private.** ✅ Reduces complexity: only
  `_reverse_map()` internally, no PEP 562 `__getattr__`, no `TYPE_CHECKING` declaration. Public surface stays
  exactly the two new functions. (Laziness is unaffected — still built on first reverse call and cached.)
- **D. Canonical correction → explicit `_CANONICAL_OVERRIDES` table.** ✅ Self-documenting and robust to future
  dict re-sorting; the source dict is left untouched.

## 10. Optional / future (out of scope for #9)

- **CLI reverse lookup.** Could add `content-types --ext application/pdf` → `.pdf`. Kept out of the core
  change because auto-detecting "is this arg a MIME type?" is ambiguous (paths contain `/` too), so it'd need
  an explicit flag. Flag if desired.
- A `fallback=` param on `guess_extension` (mirroring `get_content_type`) — intentionally omitted now;
  callers can write `guess_extension(t) or '.bin'`. Can be added later without breaking the `Optional[str]`
  contract.

## 11. Verification provenance

The hard parts of this plan were checked empirically against the live dict (via `venv/bin/python`) and
adversarially re-verified by an independent pass: the 364/223/57 counts, the 4-row override set (no missed
candidates among all 57 groups), the fallback-bucket policy, and the round-trip invariant
(`get_content_type(guess_extension(t)) == t`, 0 failures across all 223 types).
