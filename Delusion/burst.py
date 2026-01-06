try:
    from .delusion import activate_delusion
except ImportError:
    from Delusion.delusion import activate_delusion

subjects = [
    {"name": "Childe", "age": 23, "vis": True, "eff": 0.65, "color": "#e67e22"},
    {"name": "Arlecchino", "age": 30, "vis": True, "eff": 0.95, "color": "#c0392b"},
    {"name": "Foolish NPC", "age": 16, "vis": False, "eff": 0.05, "color": "#7f8c8d"}
]

if __name__ == "__main__":
    activate_delusion("Childe", 23, True, 0.65)
    print("--------------------------------")
    activate_delusion("Arlecchino", 30, True, 0.95)
    print("--------------------------------")
    activate_delusion("Foolish NPC", 16, False, 0.05)
    print("--------------------------------")
