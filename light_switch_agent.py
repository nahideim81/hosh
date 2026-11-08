# عامل ساده واکنشی (Simple Reflex Agent)
# محیط: شبکه 2 در 2 که هر خانه يك چراغ دارد
# هدف: خاموش كردن تمام خانه‌هاي روشن

# ---------------------------------------------------------------
# 1) تعريف محيط (Environment)
# ---------------------------------------------------------------
class LightEnvironment:
    def __init__(self):
        # True  = چراغ روشن   |   False = چراغ خاموش
        self.lights = [
            [True,  True],
            [True,  False],
        ]
        # موقعيت اوليه عامل: (ردیف, ستون)
        self.agent_pos = (0, 0)

    # ادراك (Percept): عامل فقط وضعيت خانه‌ي كنوني خودش را مي‌بيند
    def percept(self):
        r, c = self.agent_pos
        return {"pos": self.agent_pos, "light_on": self.lights[r][c]}

    # اجراي عمل (Action)
    def do_action(self, action, pos):
        r, c = pos
        if action == "TURN_OFF":
            self.lights[r][c] = False
        elif action == "MOVE":          # عامل در حلقه‌ي ثابت 4 خانه‌اي جلو مي‌رود
            order = [(0, 0), (0, 1), (1, 1), (1, 0)]
            i = order.index(self.agent_pos)
            self.agent_pos = order[(i + 1) % len(order)]

    # آيا هدف محقق شده؟ (تمام چراغ‌ها خاموش هستند)
    def goal_reached(self):
        return not any(cell for row in self.lights for cell in row)

    # نمايش محيط
    def show(self, step):
        print(f"--- گام {step} ---")
        for r in range(2):
            line = ""
            for c in range(2):
                mark = "*" if (r, c) == self.agent_pos else " "
                bulb = "روشن" if self.lights[r][c] else "خاموش"
                line += f"[{bulb}{mark}] "
            print(line)
        print()


# ---------------------------------------------------------------
# 2) تعريف عامل (Agent) — قاعده حس/عمل
# ---------------------------------------------------------------
class SimpleReflexAgent:
    # مسير ثابت بازديد از همه‌ي خانه‌ها
    PATH = [(0, 0), (0, 1), (1, 1), (1, 0)]

    def decide(self, percept):
        # قاعده: اگر چراغ خانه‌ي كنوني روشن است => خاموشش كن
        if percept["light_on"]:
            return "TURN_OFF"
        # قاعده: در غير اين صورت => به خانه‌ي بعدي برو
        return "MOVE"


# ---------------------------------------------------------------
# 3) حلقه‌ي اصلي: ادراك -> انديشيدن -> عمل
# ---------------------------------------------------------------
def run():
    # تنظيم كدگذاری کنسول براي نمايش فارسي در ويندوز
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    env = LightEnvironment()
    agent = SimpleReflexAgent()

    step = 0
    max_steps = 20          # جلوي حلقه‌ي نامحدود را مي‌گيرد

    env.show(step)
    while not env.goal_reached() and step < max_steps:
        p = env.percept()                    # 1) ادراك
        action = agent.decide(p)             # 2) انديشيدن (قاعده‌ي واکنشی)
        env.do_action(action, p["pos"])      # 3) عمل
        step += 1
        print(f"ادراك: خانه {p['pos']} چراغ {'روشن' if p['light_on'] else 'خاموش'}"
              f"  ->  عمل: {action}")
        env.show(step)

    if env.goal_reached():
        print("✔ هدف محقق شد: تمام خانه‌ها خاموش شدند!")
    else:
        print("✘ هدف در مهلت مقرر محقق نشد.")


if __name__ == "__main__":
    run()