from typing import Tuple, Type, TypeVar
from dataclasses import fields, make_dataclass

T = TypeVar("T")

def map_row_to_model(row: Tuple, column_names: list[str], model_class: Type[T]) -> T:
    """
    Mappt eine Datenbank-Zeile (row) in eine Instanz der angegebenen Dataclass (model_class).
    """
    row_dict = dict(zip(column_names, row))
    model_fields = {f.name for f in fields(model_class)}
    filtered_dict = {k: v for k, v in row_dict.items() if k in model_fields}
    return model_class(**filtered_dict)