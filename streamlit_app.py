import streamlit as st
import pandas as pd
from aurora_dsql import DSQLConnection
from time import sleep
import random

st.set_page_config(
    page_title="Agendamento",
    page_icon="🗓️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    /* Brand colors */
    :root {
        --white: #ffffff;
        --light-gray: #b0b0b0;
        --brand-green: #8eb6a7;
        --dark-green: #637970;
        --black: #111111;
    }
    
    /* Page background */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--dark-green);
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: var(--brand-green);
        color: var(--white);
        border: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: var(--dark-green);
        color: var(--white);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: var(--white);
        border-right: 1px solid #f0f0f0;
    }
    
    /* Dividers */
    hr {
        border-top: 1px solid var(--light-gray);
        margin: 1.5rem 0;
    }
    
    /* Info box */
    .stInfo {
        background-color: rgba(142, 182, 167, 0.2);
        border: 1px solid var(--brand-green);
        border-radius: 4px;
    }
    
    /* Warning box */
    .stWarning {
        border-radius: 4px;
    }
    
    /* Selected time highlight */
    .selected-time {
        font-weight: bold;
        color: var(--dark-green);
        margin: 1rem 0;
        padding: 0.5rem;
        background-color: rgba(142, 182, 167, 0.1);
        border-radius: 4px;
        border-left: 4px solid var(--brand-green);
    }
    
    /* Section containers */
    .shift-container {
        background-color: var(--white);
        padding: 1rem;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def dsql_conn():
    return DSQLConnection(
        access_key=st.secrets["AWS_ACCESS_KEY"],
        secret_key=st.secrets["AWS_SECRET_KEY"],
        region=st.secrets["REGION"],
        hostname=st.secrets["HOSTNAME"],
        database=st.secrets["DATABASE"],
        username=st.secrets["USERNAME"],
    )


aurora_dsql = dsql_conn()

# Initialize session state variables
if "time_slot" not in st.session_state:
    st.session_state["time_slot"] = ""
if "employee_name" not in st.session_state:
    st.session_state["employee_name"] = ""
if "is_disabled" not in st.session_state:
    st.session_state["is_disabled"] = False

with st.sidebar:
    st.logo(
        r"https://static.wixstatic.com/media/5ef07f_6416d9829dc4405385d15d6ca52bd186~mv2.png/v1/fill/w_108,h_35,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/5ef07f_6416d9829dc4405385d15d6ca52bd186~mv2.png",
        link="https://www.talst.com.br",
    )

    st.markdown("### Novo Agendamento")
    st.markdown("Selecione o seu nome e um horário disponível")

    names = aurora_dsql.get_nonbooked_employees()
    if names:
        opt = st.selectbox("Selecione o seu nome", options=names)

        if st.session_state.time_slot != "":
            st.markdown(
                f"""
            <div class='selected-time'>
                Horário selecionado: {st.session_state.time_slot}
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.session_state.is_disabled = True
            sleep(random.randint(2, 3))
            st.session_state.is_disabled = False
            # Simplified direct booking - no dialog
            if st.button(
                "Confirmar Agendamento",
                key="confirm_sidebar",
                disabled=st.session_state.is_disabled,
            ):
                st.session_state.employee_name = opt
                st.session_state.is_disabled = True
                aurora_dsql.update_employee_booking(
                    st.session_state.employee_name, st.session_state.time_slot
                )
        else:
            st.warning("Selecione um horário disponível")
    else:
        st.info("Não há nomes disponíveis para agendamento")

st.title("Agendamento de Horários")
st.markdown("Selecione um horário disponível nos turnos abaixo:")


response = aurora_dsql.get_booked_employees()
df = pd.DataFrame(response, columns=["name", "booked", "scheduled_time"])

TIME_SLOTS = {
    "first_shift": ["11:50:00", "12:10:00", "12:30:00"],
    "second_shift": ["13:02:00", "13:22:00", "13:42:00"],
}

st.markdown(
    """
<div class='shift-container'>
    <h3>Primeiro Turno</h3>
""",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:
    if (df["scheduled_time"] == "11:50:00").sum() <= 10:
        remaining = 10 - (df["scheduled_time"] == "11:50:00").sum()
        st.markdown(f"**Vagas disponíveis:** {remaining}")
        if st.button("11:50", key="113000"):
            st.session_state.time_slot = "11:50:00"
            st.rerun()
    else:
        st.error("Horário indisponível")

with col2:
    if (df["scheduled_time"] == "12:10:00").sum() <= 10:
        remaining = 10 - (df["scheduled_time"] == "12:10:00").sum()
        st.markdown(f"**Vagas disponíveis:** {remaining}")
        if st.button("12:10", key="121000"):
            st.session_state.time_slot = "12:10:00"
            st.rerun()
    else:
        st.error("Horário indisponível")

with col3:
    if (df["scheduled_time"] == "12:30:00").sum() <= 10:
        remaining = 10 - (df["scheduled_time"] == "12:30:00").sum()
        st.markdown(f"**Vagas disponíveis:** {remaining}")
        if st.button("12:30", key="123000"):
            st.session_state.time_slot = "12:30:00"
            st.rerun()
    else:
        st.error("Horário indisponível")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
<div class='shift-container'>
    <h3>Segundo Turno</h3>
""",
    unsafe_allow_html=True,
)

col4, col5, col6 = st.columns(3)

with col4:
    if (df["scheduled_time"] == "13:02:00").sum() <= 10:
        remaining = 10 - (df["scheduled_time"] == "13:02:00").sum()
        st.markdown(f"**Vagas disponíveis:** {remaining}")
        if st.button("13:02", key="130200"):
            st.session_state.time_slot = "13:02:00"
            st.rerun()
    else:
        st.error("Horário indisponível")

with col5:
    if (df["scheduled_time"] == "13:22:00").sum() <= 10:
        remaining = 10 - (df["scheduled_time"] == "13:22:00").sum()
        st.markdown(f"**Vagas disponíveis:** {remaining}")
        if st.button("13:22", key="132200"):
            st.session_state.time_slot = "13:22:00"
            st.rerun()
    else:
        st.error("Horário indisponível")

with col6:
    if (df["scheduled_time"] == "13:42:00").sum() <= 10:
        remaining = 10 - (df["scheduled_time"] == "13:42:00").sum()
        st.markdown(f"**Vagas disponíveis:** {remaining}")
        if st.button("13:42", key="134200"):
            st.session_state.time_slot = "13:42:00"
            st.rerun()
    else:
        st.error("Horário indisponível")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### Agendamentos Confirmados")


st.dataframe(
    df.loc[df["scheduled_time"] == st.session_state.time_slot],
    hide_index=True,
    use_container_width=True,
)

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: var(--light-gray); font-size: 12px; margin-top: 2rem;">
        © 2025 TALST - Todos os direitos reservados
    </div>
    """,
    unsafe_allow_html=True,
)
