# Validation lifecycle reference

This directory demonstrates issue #43's ownership boundary.

- `core-valid-domain-invalid.dodge.json` is valid DODGE 0.2.1 but intentionally violates the Wretched Demesne semantic profile: it marks a room searchable without providing executable Search semantics.
- `validate_wretched.py` first runs the DODGE core schema, then runs the WD-owned domain rule and confirms that the fixture is rejected before resolution or target generation.

The `wretched-demesne:searchable` extension is deliberately not part of the generic schema. DODGE specifies the profile declaration and gated lifecycle; WD specifies the meaning and validation of its extension.

Run from the repository root:

```sh
python draft/v0.2.1/examples/validation-lifecycle/validate_wretched.py
```
