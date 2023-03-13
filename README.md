# Pydantic Dict Encoders

Simple wrapper of pydantic for support custom dict encoders like json encoders

[![CI](https://github.com/i8enn/pydantic_dict_encoders/actions/workflows/testing.yml/badge.svg?branch=master)](https://github.com/i8enn/pydantic_dict_encoders/actions?query=branch%3Amaster+workflow%3Atesting)
[![Coverage](https://codecov.io/gh/i8enn/pydantic_dict_encoders/branch/master/graph/badge.svg?token=TER6OGX2Z7)](https://codecov.io/gh/i8enn/pydantic_dict_encoders)
[![pypi](https://img.shields.io/pypi/v/pydantic_dict_encoders.svg)](https://pypi.python.org/pypi/pydantic_dict_encoders)
[![downloads](https://pepy.tech/badge/pydantic_dict_encoders/month)](https://pepy.tech/project/pydantic_dict_encoders)
[![versions](https://img.shields.io/pypi/pyversions/pydantic_dict_encoders.svg)](https://github.com/i8enn/pydantic_dict_encoders)
[![license](https://img.shields.io/github/license/i8enn/pydantic_dict_encoders.svg)](https://github.com/i8enn/pydantic_dict_encoders/blob/master/LICENSE)


This wrapper created for solve serialization problem in ariadne resolvers, where needed return dict only with simple objects.
After research [some problems](https://github.com/pydantic/pydantic/issues/1409) and pydantic features, it was decided to make this wrapper more like a crutch for solve my problem.

This should be resolved in [Pydantic V2](https://github.com/pydantic/pydantic/discussions/4456), but it's not production ready yet.
And even there is a [PR](https://github.com/pydantic/pydantic/pull/4978) that was made some time ago. But for now, it seemed to me sufficient to use this solution and perhaps it will be useful to someone else.

*Thanks to @samuelcolvin for create and being active on pydantic and starting to solve problems before some people think about them! :)*

> **IMPORTANT!** Remember: this is a crutch that you use at your own risk. It will most likely not be needed after some time, but if everything suits you - go for it ;)

---

## Usage

This wrapper has 2 possibilities:

1. Define custom dict encoders that work the same as pydantic [`json_encoders`](https://docs.pydantic.dev/usage/exporting_models/#json_encoders) when calling `model.dict()`
2. Encode each field value as if they were passed to pydantic json.

To use this just inherit your model from `PydanticDictEncodersMixin`:

```python
class AnyModel(PydanticDictEncodersMixin, BaseModel):
    any_field: str | None = None

    class Config:
        dict_encoders = {}
        jsonify_dict_encode = False
```

> **WARNING!** Please, remember about python MRO: BaseModel MUST BE after mixin.

---
## Pros and cons

### Pros:
- Pretty simple and fast way to get the required behavior when exporting to a python dict

### Cons:
- In nested models that do not inherit from the mixin, serialization will break
- Dirty decision
