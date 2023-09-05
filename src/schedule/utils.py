from typing import List

def delete_empty_elements(array: List[str]) -> List[str]:
    if array[0] == '' and array[len(array)-1] == '':
        array.pop(0)
        array.pop(len(array) - 1)
    return array