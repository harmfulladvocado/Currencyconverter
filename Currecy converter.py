import re

RATES_TO_EUR = {
    "USD": 0.87,  "GBP": 1.15,  "EUR": 1.00,  "JPY": 0.0065, "AUD": 0.59,
    "BGN": 0.51,  "CZK": 0.041, "CAD": 0.68,  "CHF": 1.01,  "SEK": 0.087,
    "NOK": 0.083, "DKK": 0.13,  "INR": 0.011, "CNY": 0.13,  "TRY": 0.031,
    "MXN": 0.049, "BRL": 0.18,  "ZAR": 0.049, "KRW": 0.00071,"SGD": 0.66,
    "NZD": 0.57,  "PLN": 0.22,  "HUF": 0.0026,"ILS": 0.25,  "AED": 0.25,
    "SAR": 0.24,  "PHP": 0.015, "THB": 0.026, "HKD": 0.11,  "EGP": 0.029,
    "TWD": 0.027, "VND": 0.000038, "COP": 0.00022, "PEN": 0.25, "CLP": 0.0011,
    "RSD": 0.0085, "UAH": 0.023, "GEL": 0.36, "BHD": 2.45, "OMR": 2.37,
    "QAR": 0.24, "NGN": 0.0022, "KES": 0.0061
}

AVAILABLE = ", ".join(sorted(RATES_TO_EUR.keys()))

def convert(amount: float, src: str, dst: str) -> float:
    src = src.upper(); dst = dst.upper()
    if src not in RATES_TO_EUR or dst not in RATES_TO_EUR:
        raise KeyError("Unknown currency")
    eur = amount * RATES_TO_EUR[src]
    return eur / RATES_TO_EUR[dst]

def parse_input(text: str):
    text = text.strip()
    amount_first = re.search(r'^\s*([0-9\.,]+)\s*([A-Za-z]{3})\s*(?:to)?\s*([A-Za-z]{3})\s*$', text, re.I)
    if amount_first:
        amt, a, b = amount_first.groups()
        return amt, a.upper(), b.upper()
    alt = re.search(r'^\s*([A-Za-z]{3})\s*([0-9\.,]+)\s*(?:to)?\s*([A-Za-z]{3})\s*$', text, re.I)
    if alt:
        a, amt, b = alt.groups()
        return amt, a.upper(), b.upper()
    return None

def sanitate_number(s: str) -> float:
    s = s.strip().replace(" ", "")
    if s.count(",") == 1 and s.count(".") == 0:
        s = s.replace(",", ".")
    else:
        s = s.replace(",", "")
    return float(s)

def fmt(n: float) -> str:
    return format(n, ",.2f")

def main():
    print("Currency converter. Available:", AVAILABLE)
    print("Enter examples: '100 USD to EUR', 'USD 100 EUR' or type 'quit' to exit.\n")
    while True:
        line = input("> ").strip()
        if not line or line.lower() in ("quit", "exit"):
            break
        parsed = parse_input(line)
        if not parsed:
            print("Couldn't parse input. Example: '100 USD to EUR'")
            continue
        amt_str, src, dst = parsed
        try:
            amount = sanitate_number(amt_str)
        except ValueError:
            print("Invalid number:", amt_str)
            continue
        if src not in RATES_TO_EUR:
            print(f"Unknown source currency '{src}'. Available: {AVAILABLE}")
            continue
        if dst not in RATES_TO_EUR:
            print(f"Unknown destination currency '{dst}'. Available: {AVAILABLE}")
            continue
        try:
            result = convert(amount, src, dst)
        except Exception as e:
            print("Conversion error:", e)
            continue
        print(f"{fmt(amount)} {src} = {fmt(result)} {dst}")

if __name__ == "__main__":
    main()
