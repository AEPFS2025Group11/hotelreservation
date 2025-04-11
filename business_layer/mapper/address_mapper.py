from typing import Type, TypeVar, Any

from marshmallow import Schema

T = TypeVar('T')


def map_to_entity(schema: Schema, entity_cls: Type[T], data: dict, **extra_fields) -> T:
    validated_data = schema.load(data)
    return entity_cls(**validated_data, **extra_fields)


def map_to_dict(schema: Schema, entity: Any) -> dict:
    return schema.dump(vars(entity))
