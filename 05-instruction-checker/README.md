# Instruction Following Checker

When a user writes "answer in under 100 words, use 3 bullets, and return valid JSON", you can test that automatically. This project does that. It checks word count, bullet count, required and forbidden text, and JSON validity.

**Skills shown:** instruction-following evaluation, writing precise pass/fail criteria, debugging failing cases.

## Run the tests

```
python3 -m unittest -v
```

## Example

```python
from constraints import Constraints, check

rules = Constraints(max_words=100, bullet_count=3, must_avoid=("as an AI",))
print(check(model_answer, rules))  # [] means it passed
```
