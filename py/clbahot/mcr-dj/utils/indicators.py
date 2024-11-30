# utils/indicators.py

def update_indicator(indicator, state):
    color = "green" if state else "red"
    indicator.itemconfig(indicator.find_withtag("circle"), fill=color)
