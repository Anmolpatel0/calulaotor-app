
import math
import requests
import streamlit as st

st.set_page_config(
    page_title="CalcFlow | Smart Calculator",
    page_icon="🧮",
    layout="wide",
)

# ---------- Aesthetic UI ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at top left, #252451, transparent 45%),
        #0b1020;
    color: #f4f6ff;
    font-family: 'Manrope', sans-serif;
}
[data-testid="stSidebar"] {
    background: #111831;
}
.hero {
    padding: 30px;
    border-radius: 24px;
    background: linear-gradient(120deg, #29245b, #143b48);
    border: 1px solid #44456c;
    margin-bottom: 24px;
}
.hero h1 {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
}
.hero p { color: #c5c9e5; }
.result {
    padding: 24px;
    margin-top: 16px;
    border-radius: 18px;
    background: linear-gradient(120deg, #342b70, #164c51);
    border: 1px solid #6660b5;
}
.result-label {
    color: #c5c9e5;
    font-size: 13px;
}
.result-value {
    font-size: 32px;
    font-weight: 800;
    overflow-wrap: anywhere;
}
div.stButton > button {
    border-radius: 12px;
    min-height: 44px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# ---------- Calculator functions ----------
def calculate(a, operator, b):
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        if b == 0:
            raise ZeroDivisionError(
                "Division by zero is not allowed."
            )
        return a / b
    else:
        raise ValueError("Invalid operator.")


def convert_units(value, conversion):
    conversions = {
        "Kilometers to Miles": (
            value * 0.621371, "miles"
        ),
        "Miles to Kilometers": (
            value / 0.621371, "km"
        ),
        "Celsius to Fahrenheit": (
            value * 9 / 5 + 32, "°F"
        ),
        "Fahrenheit to Celsius": (
            (value - 32) * 5 / 9, "°C"
        ),
        "Kilograms to Pounds": (
            value * 2.2046226218, "lb"
        ),
        "Pounds to Kilograms": (
            value / 2.2046226218, "kg"
        ),
        "Centimeters to Inches": (
            value / 2.54, "in"
        ),
        "Inches to Centimeters": (
            value * 2.54, "cm"
        ),
        "Liters to US Gallons": (
            value * 0.2641720524, "US gal"
        ),
        "US Gallons to Liters": (
            value / 0.2641720524, "L"
        ),
    }

    return conversions[conversion]


@st.cache_data(ttl=1800)
def get_exchange_rate(base, target):
    if base == target:
        return 1.0, "same currency"

    url = (
        "https://api.frankfurter.app/latest"
        f"?from={base}&to={target}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    rate = data.get("rates", {}).get(target)

    if rate is None:
        raise ValueError("Exchange rate not available.")

    return float(rate), data.get("date", "")


def show_result(label, value):
    st.markdown(
        f"""
        <div class="result">
            <div class="result-label">{label}</div>
            <div class="result-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Header ----------
st.markdown("""
<div class="hero">
    <div style="color:#aaa4ff; letter-spacing:3px;">
        SMART TOOLS • SIMPLE MATH
    </div>
    <h1>🧮 CalcFlow</h1>
    <p>
        Calculate. Convert. Keep moving.
        Your everyday mathematics workspace.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- Navigation ----------
page = st.sidebar.radio(
    "YOUR WORKSPACE",
    [
        "Calculator",
        "Unit Converter",
        "Currency Exchange",
        "About",
    ],
)

st.sidebar.divider()
st.sidebar.caption("Built with Python + Streamlit")
st.sidebar.caption("Beginner-friendly learning project")

# ---------- Calculator ----------
if page == "Calculator":
    st.subheader("✦ Basic Calculator")
    st.write("Perform arithmetic operations instantly.")

    col1, col2 = st.columns(2)

    with col1:
        a = st.number_input(
            "First number", value=12.0, key="first"
        )

    with col2:
        b = st.number_input(
            "Second number", value=3.0, key="second"
        )

    operator = st.radio(
        "Choose operation",
        ["+", "-", "*", "/"],
        horizontal=True,
    )

    if st.button(
        "Calculate result →",
        type="primary",
        use_container_width=True,
    ):
        try:
            result = calculate(a, operator, b)

            if math.isfinite(result):
                show_result(
                    "YOUR RESULT",
                    f"{result:,.10g}",
                )
            else:
                st.error("Result is outside the supported range.")

        except (ValueError, ZeroDivisionError) as error:
            st.error(str(error))
        except OverflowError:
            st.error("The result is too large.")

    with st.expander("Learn the Python logic"):
        st.code("""
def calculate(a, operator, b):
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        if b == 0:
            raise ZeroDivisionError
        return a / b
""", language="python")

# ---------- Unit Converter ----------
elif page == "Unit Converter":
    st.subheader("↗ Unit Converter")
    st.write("Convert measurements with simple formulas.")

    conversion = st.selectbox(
        "Conversion type",
        [
            "Kilometers to Miles",
            "Miles to Kilometers",
            "Celsius to Fahrenheit",
            "Fahrenheit to Celsius",
            "Kilograms to Pounds",
            "Pounds to Kilograms",
            "Centimeters to Inches",
            "Inches to Centimeters",
            "Liters to US Gallons",
            "US Gallons to Liters",
        ],
    )

    value = st.number_input(
        "Value to convert", value=10.0
    )

    if st.button(
        "Convert units →",
        type="primary",
        use_container_width=True,
    ):
        result, unit = convert_units(
            value, conversion
        )

        show_result(
            conversion.upper(),
            f"{result:,.10g} {unit}",
        )

    with st.expander("Conversion formulas"):
        st.markdown("""
        - km → miles: multiply by `0.621371`
        - °C → °F: `(C × 9/5) + 32`
        - kg → lb: multiply by `2.20462`
        - cm → inches: divide by `2.54`
        - liters → US gallons: multiply by `0.264172`
        """)

# ---------- Currency Exchange ----------
elif page == "Currency Exchange":
    st.subheader("◎ Currency Exchange")
    st.write(
        "Get reference exchange rates from a public API."
    )

    currencies = {
        "USD — US Dollar": "USD",
        "INR — Indian Rupee": "INR",
        "EUR — Euro": "EUR",
        "GBP — British Pound": "GBP",
        "JPY — Japanese Yen": "JPY",
        "CAD — Canadian Dollar": "CAD",
        "AUD — Australian Dollar": "AUD",
        "CHF — Swiss Franc": "CHF",
        "CNY — Chinese Yuan": "CNY",
        "SGD — Singapore Dollar": "SGD",
        "NZD — New Zealand Dollar": "NZD",
        "BRL — Brazilian Real": "BRL",
        "MXN — Mexican Peso": "MXN",
        "ZAR — South African Rand": "ZAR",
        "THB — Thai Baht": "THB",
        "KRW — South Korean Won": "KRW",
    }

    col1, col2 = st.columns(2)

    with col1:
        from_label = st.selectbox(
            "From currency", list(currencies.keys())
        )

    with col2:
        to_label = st.selectbox(
            "To currency",
            list(currencies.keys()),
            index=1,
        )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        value=100.0,
        step=10.0,
    )

    if st.button(
        "Convert currency →",
        type="primary",
        use_container_width=True,
    ):
        base = currencies[from_label]
        target = currencies[to_label]

        try:
            with st.spinner("Fetching exchange rate..."):
                rate, rate_date = get_exchange_rate(
                    base, target
                )

            converted = amount * rate

            show_result(
                f"{amount:g} {base} → {target}",
                f"{converted:,.4f} {target}",
            )

            st.caption(
                f"Reference rate: 1 {base} = "
                f"{rate:.6g} {target}. "
                f"Rate date: {rate_date}"
            )

        except requests.RequestException:
            st.error(
                "Network error. Check your internet "
                "connection and try again."
            )
        except (ValueError, KeyError):
            st.error(
                "Rate unavailable for this currency pair."
            )

    st.caption(
        "Rates are for reference only and may differ "
        "from bank or payment-provider rates."
    )

# ---------- About ----------
elif page == "About":
    st.subheader("About CalcFlow")

    st.write("""
    CalcFlow is a beginner-friendly Python project.

    **What you can learn:**
    - Python functions and return values
    - If/elif/else conditionals
    - Exception handling and validation
    - HTTP requests and JSON parsing
    - Streamlit interface development
    """)

    st.info(
        "Next challenge: build a command-line version "
        "using input(), functions, and while loops."
    )

st.divider()
st.caption(
    "CALCFLOW • Python + Streamlit • "
    "Made for learning and everyday calculations"
)
