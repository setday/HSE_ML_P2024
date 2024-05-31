from tests.TestCore import TestCore


def run_load_tests():
    # params = input("Enter testing type and list of objects:\n").split()
    core = TestCore(
        "graphics",
        ["car", "cone", "tree", "metal_pipe", "rubbish_line", "parking_place"],
    )
    core.run()


if __name__ == "__main__":
    run_load_tests()
