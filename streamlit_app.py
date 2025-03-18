import streamlit as st
from supabase import create_client
import pandas as pd

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
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase = init_connection()
if "time_slot" not in st.session_state:
    st.session_state["time_slot"] = ""


def get_employee_names():
    """Get list of employee names that haven't been booked yet"""
    result = supabase.table("employees").select("name").eq("booked", False).execute()

    if not result.data:
        return []

    names = [employee["name"] for employee in result.data]
    return names


@st.dialog("Confirme as informações")
def confirm_booking(opt: str):
    st.markdown("### Confirmação de Agendamento")
    st.markdown(f"**Nome:** {opt}")
    st.markdown(f"**Horário:** {st.session_state.time_slot}")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Confirmar", key="confirm_dialog"):
            (
                supabase.table("employees")
                .update({"booked": True, "scheduled_time": st.session_state.time_slot})
                .eq("name", opt)
                .execute()
            )
            st.success("Agendamento confirmado com sucesso!")
            st.rerun()


with st.sidebar:
    st.logo(
        r"https://static.wixstatic.com/media/5ef07f_6416d9829dc4405385d15d6ca52bd186~mv2.png/v1/fill/w_108,h_35,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/5ef07f_6416d9829dc4405385d15d6ca52bd186~mv2.png",
        link="https://www.talst.com.br",
    )

    st.markdown("### Novo Agendamento")
    st.markdown("Selecione o seu nome e um horário disponível")

    names = get_employee_names()
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

            if st.button("Confirmar Agendamento", key="confirm_sidebar"):
                confirm_booking(opt)
        else:
            st.warning("Selecione um horário disponível")
    else:
        st.info("Não há nomes disponíveis para agendamento")

st.title("Agendamento de Horários")
st.markdown("Selecione um horário disponível nos turnos abaixo:")

response = supabase.table("employees").select("*").execute()
df = pd.DataFrame(response.data)

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

filtered_df = df.loc[df["scheduled_time"] == st.session_state.time_slot]
filtered_df.columns = ["Nome", "Agendado", "Horário"]
filtered_df = filtered_df.drop(columns="Agendado")

if not filtered_df.empty:
    styled_df = filtered_df.style.set_properties(
        **{
            "background-color": "#f8faf9",
            "color": "#111111",
            "border": "1px solid #e6e6e6",
            "text-align": "left",
            "font-size": "14px",
            "padding": "8px",
        }
    ).set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("background-color", "#8eb6a7"),
                    ("color", "white"),
                    ("font-weight", "bold"),
                    ("text-align", "left"),
                    ("font-size", "16px"),
                    ("padding", "10px"),
                ],
            },
            {
                "selector": "tr:hover",
                "props": [
                    ("background-color", "#e6f0eb"),
                ],
            },
        ]
    )

    st.dataframe(styled_df, hide_index=True, use_container_width=True)
else:
    st.info("Nenhum agendamento marcado para este horário.")

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: var(--light-gray); font-size: 12px; margin-top: 2rem;">
        © 2025 TALST - Todos os direitos reservados
    </div>
    """,
    unsafe_allow_html=True,
)
