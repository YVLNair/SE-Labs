# SE Lab 7: Fuzz Testing

Hypothesis tests exercise rider specifications, dispatch throughput metrics, and safety restraint codes with generated Unicode strings and `None` values. The processor returns useful error messages for malformed inputs instead of raising parsing or lookup exceptions.

## Run

```powershell
python -m pip install -r requirements.txt
python -m pytest -v test_processor.py
python processor.py
```

The fuzz tests check that malformed values never escape as exceptions. The additional examples check normal results and invalid throughput values such as zero-duration cycles, non-finite numbers, and overflow.
