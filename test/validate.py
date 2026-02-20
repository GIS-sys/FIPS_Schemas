from typing import Any


def get_control_ogrn(t: str, value: str) -> str:
    if t == "UL":
        main = value[:12]
        control = (int(main) % 11) % 10
        return str(control)
    if t == "IP":
        main = value[:14]
        control = (int(main) % 13) % 10
        return str(control)
    raise Exception(f"get_control_ogrn expected t in [UL, IP], got {t}")

def get_control_snils(value: str) -> str:
    main = value[:9]
    control = 0
    for i, d in enumerate(main):
        control += int(d) * (9 - i)
    control = (control % 101)
    if control >= 100:
        control = 0
    return ("0" + str(control))[-2:]

def get_control_inn(t: str, value: str) -> str:
    if t == "UL":
        main = value[:9]
        control = 0
        for i, d in enumerate(main):
            control += int(d) * [2, 4, 10, 3, 5, 9, 4, 6, 8][i]
        control = (control % 11) % 10
        return str(control)
    if t == "IP" or t == "FL":
        main = value[:10]
        control1 = 0
        for i, d in enumerate(main):
            control1 += int(d) * [7, 2, 4, 10, 3, 5, 9, 4, 6, 8][i]
        control1 = (control1 % 11) % 10
        control2 = 0
        for i, d in enumerate(main + str(control1)):
            control2 += int(d) * [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8][i]
        control2 = (control2 % 11) % 10
        return str(control1) + str(control2)
    raise Exception(f"get_control_inn expected t in [FL, UL, IP], got {t}")





def validate_ogrn(t: str, value: str) -> str:
    if value is None:
        return False
    if t == "UL":
        return len(value) == 13 and value[-1] == get_control_ogrn(t, value)
    if t == "IP":
        return len(value) == 15 and value[-1] == get_control_ogrn(t, value)
    raise Exception(f"validate_ogrn expected t in [UL, IP], got {t}")

def validate_snils(value: str) -> str:
    if value is None:
        return False
    return len(value) == 11 and value[-2:] == get_control_snils(value)

def validate_inn(t: str, value: str) -> str:
    if value is None:
        return False
    if t == "UL":
        return len(value) == 10 and value[-1] == get_control_inn(t, value)
    if t == "FL" or t == "IP":
        return len(value) == 12 and value[-2:] == get_control_inn(t, value)
    raise Exception(f"validate_inn expected t in [FL, UL, IP], got {t}")

def validate_kpp(value: str) -> str:
    if value is None:
        return False
    return len(value) == 9





def validate_function(validate: str, value: Any, allow_none: bool = False) -> bool:
    if str(validate).endswith("optional"):
        allow_none = True
        validate = str(validate)[:-len("optional")].strip()
    if allow_none and value is None:
        return True
    if validate == "kpp":
        return validate_kpp(value)
    if validate == "snils":
        return validate_snils(value)
    if validate == "ogrn_ip":
        return validate_ogrn("IP", value)
    if validate == "ogrn_ul":
        return validate_ogrn("UL", value)
    if validate == "inn_fl":
        return validate_inn("FL", value)
    if validate == "inn_ip":
        return validate_inn("IP", value)
    if validate == "inn_ul":
        return validate_inn("UL", value)
    return False

def validate_list_functions(validate: list[str], value: Any, allow_none: bool = False) -> bool:
    for v in validate:
        if not validate_function(v, value, allow_none):
            return False
    return True

