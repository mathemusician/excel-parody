import streamlit as st
from evaluator import parse_and_evaluate

# GUI


def main():
    cols = st.columns(5)

    first_column = cols[0]

    with first_column:
        for number in range(1, 5):
            st.text(" ")
            st.text(" ")
            st.markdown(
                f'<div style="text-align: right;">{number}</div>',
                unsafe_allow_html=True,
            )

    if "A1" not in st.session_state:
        for col, letter in zip(cols[1:], ["A", "B", "C", "D"]):
            for number in range(1, 5):
                with col:
                    if number == 1:
                        st.text_input(f"{letter}", key=f"{letter}{number}")
                    else:
                        st.text_input(
                            f"{letter}{number}",
                            key=f"{letter}{number}",
                            label_visibility="collapsed",
                        )

    else:
        for col, letter in zip(cols[1:], ["A", "B", "C", "D"]):
            for number in range(1, 5):
                with col:
                    key = f"{letter}{number}"
                    if number == 1:
                        st.text_input(
                            f"{letter}",
                            value=parse_and_evaluate(
                                st.session_state[key], st.session_state
                            ),
                            key=key,
                        )
                    else:
                        st.text_input(
                            key,
                            value=parse_and_evaluate(
                                st.session_state[key], st.session_state
                            ),
                            key=key,
                            label_visibility="collapsed",
                        )

    # st.session_state["A3"] = st.session_state["A4"]


#    A B C D
# 1
# 2
# 3
# 4


# EXCEL Parsing
# 1 + 1
# 1+1
# 7 * 2 + 4
# A1
# A1 * A2
# MIN(A1:A4)
# AVG(A1 * 2 + 4)


if __name__ == "__main__":
    main()
