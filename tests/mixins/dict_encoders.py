import json
from enum import IntEnum
from typing import Dict, List
from uuid import UUID, uuid4

import pytest
from pydantic import UUID4, BaseModel, Field

from pydantic_dict.mixins.dict_encoders import PydanticDictEncodersMixin


class TestEnum(IntEnum):
    FIRST = 1
    SECOND = 2


class TestModel(BaseModel):
    uuid: UUID4 = Field(default_factory=uuid4)
    string: str = "test_string"
    integer: int = 1
    boolean: bool = True
    enum: TestEnum = TestEnum.FIRST
    list_of_int: List[int] = Field(default_factory=lambda: [1, 2])
    dict_of_int: Dict[str, int] = Field(
        default_factory=lambda: {"first": 1, "second": 2}
    )


class TestEncoderModel(PydanticDictEncodersMixin, TestModel):
    pass


class TestJsonifyDictEncodeModel(PydanticDictEncodersMixin, TestModel):
    class Config:
        jsonify_dict_encode = True


class TestNestedJsonifyDictEncodeModel(PydanticDictEncodersMixin, BaseModel):
    children: TestJsonifyDictEncodeModel = Field(
        default_factory=lambda: TestJsonifyDictEncodeModel()
    )

    class Config:
        jsonify_dict_encode = True


class PydanticDictEncodersMixinTestCase:
    @pytest.mark.parametrize(
        "input,expected",
        [
            pytest.param(
                UUID("2f7f6ba5-966d-4cf3-9f78-6b6eaff74ffe"),
                "2f7f6ba5-966d-4cf3-9f78-6b6eaff74ffe",
            ),
            pytest.param(
                TestEnum.SECOND.value,
                str(TestEnum.SECOND.value),
            ),
            pytest.param(
                "any string",
                "any string",
            ),
            pytest.param(
                21213123123,
                "21213123123",
            ),
        ],
    )
    def test_get_values_like_json(self, input, expected) -> None:
        assert TestEncoderModel._get_value_like_json(input) == expected

    @pytest.mark.parametrize(
        "input,expected_encoder",
        [
            pytest.param(TestEnum, lambda v: v.value),
            pytest.param(UUID, lambda v: v.hex),
            pytest.param(int, lambda v: str(v)),
            pytest.param(list, lambda v: json.dumps(v)),
        ],
    )
    def test_get_value_custom_encoder(cls, input, expected_encoder) -> None:
        class TestModel(PydanticDictEncodersMixin, BaseModel):
            class Config:
                dict_encoders = {input.__class__: expected_encoder}

        encoder = TestModel._get_value_custom_encoder(input)
        assert encoder == expected_encoder

    def test_encode_with_dict_encoders(self) -> None:
        class TestDictEncoderModel(PydanticDictEncodersMixin, TestModel):
            class Config:
                dict_encoders = {
                    UUID: lambda v: v.hex,
                    IntEnum: lambda v: v.name,
                }

        data = TestDictEncoderModel()
        encoded_data = data.dict()
        assert encoded_data.get("enum") == data.enum.name
        assert encoded_data.get("uuid") == data.uuid.hex
        assert encoded_data.get("string") == data.string
        assert encoded_data.get("list_of_int") == data.list_of_int
        assert encoded_data.get("dict_of_int") == data.dict_of_int

    def test_encode_with_like_json(self) -> None:
        jsonify_model = TestJsonifyDictEncodeModel()
        encoded_data = jsonify_model.dict()
        assert encoded_data.get("uuid") == str(jsonify_model.uuid)
        assert encoded_data.get("string") == jsonify_model.string
        assert encoded_data.get("integer") == str(jsonify_model.integer)
        assert encoded_data.get("boolean") == "true"
        assert encoded_data.get("enum") == str(jsonify_model.enum.value)
        assert encoded_data.get("list_of_int") == ["1", "2"]
        encoded_dict = encoded_data.get("dict_of_int", {})
        assert encoded_dict.get("first") == "1"
        assert encoded_dict.get("second") == "2"

    def test_encode_with_nested_model(self) -> None:
        jsonify_model = TestNestedJsonifyDictEncodeModel()
        child_model = jsonify_model.children
        encoded_data = jsonify_model.dict()
        encoded_children = encoded_data.get("children", {})
        assert encoded_children
        assert encoded_children.get("uuid") == str(child_model.uuid)
        assert encoded_children.get("string") == child_model.string
        assert encoded_children.get("integer") == str(child_model.integer)
        assert encoded_children.get("boolean") == "true"
        assert encoded_children.get("enum") == str(child_model.enum.value)
        assert encoded_children.get("list_of_int") == ["1", "2"]
        encoded_dict = encoded_children.get("dict_of_int", {})
        assert encoded_dict.get("first") == "1"
        assert encoded_dict.get("second") == "2"

    def test_encode_with_nested_model_without_mixin(self) -> None:
        class TestNestedSimpleModel(PydanticDictEncodersMixin, BaseModel):
            children: TestModel = Field(default_factory=lambda: TestModel())

            class Config:
                jsonify_dict_encode = True

        data = TestNestedSimpleModel()
        encoded_data = data.dict()
        encoded_children = encoded_data.get("children", {})
        assert encoded_children
        assert encoded_children.get("uuid") == data.children.uuid
        assert encoded_children.get("enum") == data.children.enum
