from typing import Union

from schemas.laundry import LaundryCreateSchema, LaundryUpdateSchema


def convert_to_dict_and_delete_element(original_data: Union[LaundryCreateSchema, LaundryUpdateSchema]):
    converted_data = original_data.dict()
    del converted_data["laundry_machine_types"]
    return converted_data
