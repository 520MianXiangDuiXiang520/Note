def demo(code: int) -> str:
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case _:
            return "Internal Error"

def demo2(code: int) -> str:
    res = ""
    match code:
        case 200:
            res = "OK"
        case 404:
            res = "Not Found"
        case _:
            res = "Internal Error"
        # case 500:
        #     res = "Server Error"
    return res

def demo3(pos):
    match pos:
        case (0, 0):
            print("Origin")
        case (0, y):
            print(f"Y={y}")
        case (x, 0):
            print(f"X={x}")
        case (x, y):
            print(f"X={x}, Y={y}")
        case _:
            raise ValueError("Not a point")

class Player:
    def __init__(self, role: int, online: bool):
        self.role = role
        self.online = online

def demo4(p: Player):
    match p:
        case Player(role=1, online=False):
            print("role 1 offline")
        case Player(role=1, online=True):
            print("role 1 online")
        case _:
            print("not role 1")

def demo5(role: int, online: bool):
    match [Player(role, online)]:
        case []:
            print("empty player box")
        case [Player(role=role, online=False)]:
            print(f"role {role} offline")
        case [Player(role=role, online=True)]:
            print(f"role {role} online")
        case _:
            print("bad player box")

def demo6(log):
    match log:
        case ('warning', code, 40):
            print("A warning has been received.")
        case ('error', code, _):
            print(f"An error {code} occurred.")

def demo7(log):
    match log:
        case ('warning', code, 40):
            print("A warning has been received.")
        case ('error', code, _) if code in range(400, 500):
            print(f"An client error {code} occurred.")
        case ('error', code, _) if code in range(500, 600):
            print(f"An server error {code} occurred.")

if __name__ == "__main__":
    demo7(("error", 418, 80))
    demo7(("error", 512, 80))
    demo6(("error", 400, 80))
    demo5(2, False)
    print(demo(200))
    demo3((0, 1))
    demo4(Player(1, True))
