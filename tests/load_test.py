from tests.TestCore import TestCore

if __name__ == "__main__":
    # params = input("Enter testing type and list of objects:\n").split()
    core = TestCore("graphics", ["car", "cone", "tree", "metal_pipe", "rubbish_line", "parking_place"])
    core.run()
