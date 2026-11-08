import random
import sys
import io

# سازگاری با کنسول‌های ویندوز (cp1252) برای نمایش متن فارسی
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ============================================================
# محیط 2 در 2: چهار خانه به شکل ماتریس
# وضعیت هر خانه: True = کثیف، False = تمیز
# ============================================================
class Environment2x2:
    def __init__(self, dirty_map=None):
        # اگر نقشه داده نشود، به صورت تصادفی کثیف می‌شود
        if dirty_map is None:
            dirty_map = [[random.choice([True, False]) for _ in range(2)]
                         for _ in range(2)]
        self.grid = dirty_map
        self.agent_pos = (0, 0)          # موقعیت شروع عامل (سطر، ستون)
        self.steps = 0

    def is_dirty(self, pos):
        r, c = pos
        return self.grid[r][c]

    def clean(self, pos):
        r, c = pos
        self.grid[r][c] = False

    def is_all_clean(self):
        return not any(any(row) for row in self.grid)

    def display(self, note=""):
        """نمایش گرافیکی ساده محیط"""
        marks = []
        for r in range(2):
            row = []
            for c in range(2):
                if (r, c) == self.agent_pos:
                    row.append("V" if self.grid[r][c] else "v")  # V=عامل در خانه کثیف
                else:
                    row.append("*" if self.grid[r][c] else " ")  # *=کثیف
            marks.append(row)
        print(f"  [{marks[0][0]}][{marks[0][1]}]     [{marks[1][0]}][{marks[1][1]}]")
        print(f"  مرحله {self.steps:2d} | موقعیت: {self.agent_pos} | {note}")
        print("-" * 46)


# ============================================================
# عامل واکنشی ساده
# قانون:  اگر کثیف است → جارو بکش
#         اگر تمیز است  → جهت بعدی را برو (با حافظه جهت)
# ============================================================
class SimpleReflexVacuumAgent:
    # ترتیب بازدید خانه‌ها: بالا-چپ، بالا-راست، پایین-راست، پایین-چپ
    ORDER = [(0, 0), (0, 1), (1, 1), (1, 0)]

    def __init__(self):
        self.target_index = 0   # تنها حافظه: کدام خانه بعدی هدف است

    def select_action(self, env):
        """بر اساس وضعیت فعلی، یک عمل انتخاب می‌کند"""
        here = env.agent_pos

        # قانون اصلی: خانه کثیف است؟
        if env.is_dirty(here):
            return "SUCK"

        # خانه تمیز است → خانه هدف بعدی را پیدا کن
        for _ in range(4):                      # حداکثر 4 تلاش
            target = self.ORDER[self.target_index % 4]
            if target != here:
                break
            self.target_index += 1
        else:
            return "NO_OP"                      # همه‌جا تمیز است، بایست

        return self._move_towards(here, target)

    def _move_towards(self, here, target):
        """حرکت به سمت خانه هدف (حرکت مسیریابی ساده)"""
        r, c = here
        tr, tc = target
        if c < tc:
            return "RIGHT"
        if c > tc:
            return "LEFT"
        if r < tr:
            return "DOWN"
        return "UP"

    def update(self, action):
        if action == "SUCK":
            self.target_index += 1   # این خانه تمام شد، بعدی


# ============================================================
# حلقه اجرای عامل در محیط
# ============================================================
def run_agent(env, agent, max_steps=20):
    print("=" * 46)
    print("   عامل جاروبرقی واکنشی ساده - محیط 2x2")
    print("   V = عامل   * = خانه کثیف   خانه خالی = تمیز")
    print("=" * 46)
    env.display("شروع")

    while not env.is_all_clean() and env.steps < max_steps:
        env.steps += 1
        action = agent.select_action(env)
        note = ""

        # اجرای عمل روی محیط
        if action == "SUCK":
            env.clean(env.agent_pos)
            note = "جارو کشیدن ✔"
        elif action == "UP" and env.agent_pos[0] > 0:
            env.agent_pos = (env.agent_pos[0] - 1, env.agent_pos[1])
            note = "حرکت به بالا"
        elif action == "DOWN" and env.agent_pos[0] < 1:
            env.agent_pos = (env.agent_pos[0] + 1, env.agent_pos[1])
            note = "حرکت به پایین"
        elif action == "LEFT" and env.agent_pos[1] > 0:
            env.agent_pos = (env.agent_pos[0], env.agent_pos[1] - 1)
            note = "حرکت به چپ"
        elif action == "RIGHT" and env.agent_pos[1] < 1:
            env.agent_pos = (env.agent_pos[0], env.agent_pos[1] + 1)
            note = "حرکت به راست"
        else:
            note = "ایست (NO_OP)"

        agent.update(action)
        env.display(note)

    if env.is_all_clean():
        print(f"✔ خانه کاملاً تمیز شد! تعداد مراحل: {env.steps}")
    else:
        print("✖ به سقف مراحل رسیدیم.")


# ============================================================
# اجرا
# ============================================================
if __name__ == "__main__":
    # نقشه دلخواه: True یعنی کثیف
    initial = [
        [True,  False],   # (0,0) کثیف، (0,1) تمیز
        [False, True],    # (1,0) تمیز، (1,1) کثیف
    ]
    env = Environment2x2(dirty_map=initial)
    agent = SimpleReflexVacuumAgent()
    run_agent(env, agent)
