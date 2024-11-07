class_map = {
    0: "text",
    1: "diodelight_emitting",
    2: "lamp",
    3: "transformer",
    4: "capacitor", # capacitor unpolarized
    5: "resistor",
    6: "inductor",
    7: "diode",
    8: "switch",
    9: "powersource",
    10: "junction"
}

def get_class_mapping(key: int) -> str:
    return class_map[key]