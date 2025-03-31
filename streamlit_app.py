import streamlit as st
from supabase import create_client
import pandas as pd
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
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase = init_connection()

# Initialize session state variables
if "time_slot" not in st.session_state:
    st.session_state["time_slot"] = ""

# Check if we need to handle a completed booking from a previous run
if "booking_in_progress" in st.session_state and st.session_state.get(
    "booking_success", False
):
    st.sidebar.success(
        f"Agendamento confirmado com sucesso para {st.session_state.get('booking_employee', '')}!"
    )

    # Clean up session state after showing success message
    if "booking_in_progress" in st.session_state:
        del st.session_state["booking_in_progress"]
    if "booking_employee" in st.session_state:
        del st.session_state["booking_employee"]
    if "booking_success" in st.session_state:
        del st.session_state["booking_success"]
    # Keep the time_slot reset to avoid double-booking
    st.session_state.time_slot = ""


def get_employee_names():
    """Get list of employee names that haven't been booked yet"""
    try:
        result = (
            supabase.table("employees").select("name").eq("booked", False).execute()
        )

        if not result.data:
            return []

        names = [employee["name"] for employee in result.data]
        return names
    except Exception as e:
        return []


# Simplified direct booking function using session state to persist across reruns
def confirm_booking_direct(employee_name):
    try:
        # First run - store booking details and perform update
        if "booking_in_progress" not in st.session_state:
            st.session_state["booking_in_progress"] = True
            st.session_state["booking_employee"] = employee_name
            st.session_state["booking_time"] = st.session_state.time_slot

            # Add timestamp to track when the update was made
            import datetime

            current_time = datetime.datetime.now().isoformat()

            # Execute the update with timestamp
            result = (
                supabase.table("employees")
                .update(
                    {
                        "booked": True,
                        "scheduled_time": st.session_state.time_slot,
                        "last_updated": current_time,  # Add this field to your Supabase table
                        "updated_by": "scheduler_app",  # Add this field to identify source
                    }
                )
                .eq("name", employee_name)
                .execute()
            )
            sleep(random.randint(1, 5))

            # Set success flag and rerun
            st.session_state["booking_success"] = True
            st.rerun()
        elif st.session_state.get("booking_success", False):
            # Second run - show success message and clean up
            st.sidebar.success(
                f"Agendamento confirmado com sucesso para {st.session_state.booking_employee}!"
            )

            # Clean up session state
            del st.session_state["booking_in_progress"]
            del st.session_state["booking_employee"]
            del st.session_state["booking_success"]
            st.session_state.time_slot = ""

            # Don't rerun again - let the app refresh naturally next time
    except Exception as e:
        st.sidebar.error(f"Erro ao atualizar: {str(e)}")
        # Clean up session state on error
        if "booking_in_progress" in st.session_state:
            del st.session_state["booking_in_progress"]
        if "booking_employee" in st.session_state:
            del st.session_state["booking_employee"]
        if "booking_success" in st.session_state:
            del st.session_state["booking_success"]


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

            # Simplified direct booking - no dialog
            if st.button("Confirmar Agendamento", key="confirm_sidebar"):
                confirm_booking_direct(opt)
        else:
            st.warning("Selecione um horário disponível")
    else:
        st.info("Não há nomes disponíveis para agendamento")

st.title("Agendamento de Horários")
st.markdown("Selecione um horário disponível nos turnos abaixo:")

# Fetch and show all data
try:
    response = supabase.table("employees").select("*").execute()
    df = pd.DataFrame(response.data)
except Exception as e:
    df = pd.DataFrame(columns=["name", "booked", "scheduled_time"])

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

# Add safety check for DataFrame columns
if "scheduled_time" in df.columns and "name" in df.columns and "booked" in df.columns:
    filtered_df = df.loc[df["scheduled_time"] == st.session_state.time_slot]
    filtered_df = filtered_df[["name", "booked", "scheduled_time"]]
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
else:
    st.error(
        "Estrutura do banco de dados incorreta. Verifique se as colunas 'name', 'booked' e 'scheduled_time' existem."
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
