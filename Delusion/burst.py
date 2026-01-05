from delusion import activate_delusion

if __name__ == "__main__":
    activate_delusion("Childe", 23, True, 0.85, 0.47)
    print("--------------------------------")
    activate_delusion("Arlecchino", 30, True, 0.76, 0.90)
    print("--------------------------------")
    activate_delusion("Foolish NPC", 24, False, 0.80, 0.05)
    print("--------------------------------")
    activate_delusion("La Signora", 40, True, 0.90, 0.80) # is actually 500+ but appears 40
    print("--------------------------------")
    activate_delusion("Child NPC", 6, False, 0.95, 0.01)
    print("--------------------------------")
