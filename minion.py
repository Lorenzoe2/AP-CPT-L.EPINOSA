# imports and basic setup
import tkinter as tk
from tkinter import messagebox

# calculate basal metabolic rate (BMR)
def calc_bmr(gender, weight, height, age):
    g = gender.lower()
    if g in ['male', 'm']:
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif g in ['female', 'f']:
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Check gender input")  # guard

# map activity to multiplier
def activity_factor(level):
    factors = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }
    return factors.get(level.lower(), 1.2)

# total daily energy expenditure
def calc_tdee(bmr, factor):
    return bmr * factor

# protein range (g per kg)
def protein_range(w):
    return 1.6 * w, 2.2 * w

# adjust calories for goal
def adjust_for_goal(tdee, goal):
    gl = goal.lower()
    if gl == "lose":
        return tdee - 500
    elif gl == "gain":
        return tdee + 500
    else:
        return tdee

# validate and cast inputs
def validate_and_cast(fields):
    cleaned = {}
    for name, raw, caster in fields:
        if not raw:
            raise ValueError(f"{name} is required")
        try:
            val = caster(raw)
        except ValueError:
            raise ValueError(f"{name} must be a number")
        if val <= 0:
            raise ValueError(f"{name} must be positive")
        cleaned[name.lower()] = val
    return cleaned

# main calculation triggered by button
def calculate():
    try:
        fields = [
            ("Age", age_entry.get().strip(), int),
            ("Weight", weight_entry.get().strip(), float),
            ("Height", height_entry.get().strip(), float),
        ]
        nums = validate_and_cast(fields)
        age = nums['age']
        weight = nums['weight']
        height = nums['height']

        gen = gender_var.get()
        act = activity_var.get()
        goal = goal_var.get()

        bmr = calc_bmr(gen, weight, height, age)
        af = activity_factor(act)
        tdee = calc_tdee(bmr, af)
        adj = adjust_for_goal(tdee, goal)
        p_low, p_high = protein_range(weight)

        # build and display result
        res = f"BMR: {bmr:.2f} cal/day\n"
        res += f"TDEE: {tdee:.2f} cal/day\n"
        res += f"For {goal.capitalize()}: {adj:.2f} cal/day\n"
        res += f"Protein: {p_low:.1f}-{p_high:.1f}g/day"
        result_label.config(text=res)

    except Exception as e:
        messagebox.showerror("Oops", f"Check inputs: {e}")

# build GUI
root = tk.Tk()
root.title("Gym Nutri Calc")

gender_var = tk.StringVar(value="Male")
activity_var = tk.StringVar(value="Sedentary")
goal_var = tk.StringVar(value="Maintain")

# Gender
tk.Label(root, text="Gender").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.OptionMenu(root, gender_var, "Male", "Female").grid(row=0, column=1, padx=5, pady=5)

# age
tk.Label(root, text="Age (years)").grid(row=1, column=0, padx=5, pady=5, sticky="e")
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1, padx=5, pady=5)

# weight
tk.Label(root, text="Weight (kg)").grid(row=2, column=0, padx=5, pady=5, sticky="e")
weight_entry = tk.Entry(root)
weight_entry.grid(row=2, column=1, padx=5, pady=5)

# height
tk.Label(root, text="Height (cm)").grid(row=3, column=0, padx=5, pady=5, sticky="e")
height_entry = tk.Entry(root)
height_entry.grid(row=3, column=1, padx=5, pady=5)

# Activity
tk.Label(root, text="Activity").grid(row=4, column=0, padx=5, pady=5, sticky="e")
tk.OptionMenu(root, activity_var, "Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active").grid(row=4, column=1, padx=5, pady=5)

# goal
tk.Label(root, text="Goal").grid(row=5, column=0, padx=5, pady=5, sticky="e")
tk.OptionMenu(root, goal_var, "Lose", "Maintain", "Gain").grid(row=5, column=1, padx=5, pady=5)

# calculate Button
tk.Button(root, text="Calculate", command=calculate).grid(row=6, column=0, columnspan=2, pady=10)

# Result Label
result_label = tk.Label(root, text="", justify="left")
result_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# start GUI loop
root.mainloop()