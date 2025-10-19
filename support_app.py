import streamlit as st
from utils import response_generator, support_function

st.set_page_config(
    page_title="Eniola Healthcare Center",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        background-color: #f0f8ff;
    }
    </style>
    """, unsafe_allow_html=True)


st.title("Eniola Healthcare Center")
st.markdown("Your Health, Our Priority | 08085017583 | Ayorindesaheed2003@gmail.com")
st.markdown("---")

with st.sidebar:
    st.header("About Us")
    st.write("Location: 23 Bashorun Ojoo Road, Sango, Ibadan")
    st.write("Hours: Mon-Fri: 8AM-8PM")
    st.write("Saturday: 9AM-6PM")
    st.write("Sunday: Closed")
    
    st.markdown("---")
    st.subheader("Quick Actions")
    
    if st.button("Book Appointment"):
        st.session_state.quick_action = "I want to book an appointment"
        st.rerun()
    
    if st.button(" Order Medicine"):
        st.session_state.quick_action = "I want to order medicine"
        st.rerun()
    
    if st.button(" Lab Tests"):
        st.session_state.quick_action = "What lab tests do you offer?"
        st.rerun()
    
    if st.button(" Clear Chat"):
        st.session_state.messages = []
        st.session_state.initialized = False
        st.rerun()


if "messages" not in st.session_state:
    st.session_state.messages = []

if "initialized" not in st.session_state:
    st.session_state.initialized = False

if "quick_action" not in st.session_state:
    st.session_state.quick_action = None


if not st.session_state.initialized and len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        greeting_prompt = "You are starting a new conversation. Greet the customer warmly and ask how you can help them. Keep it brief (2-3 sentences max)."
        greeting = support_function(greeting_prompt, chat_history=[])
        st.markdown(greeting)
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    st.session_state.initialized = True


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if st.session_state.quick_action:
    prompt = st.session_state.quick_action
    st.session_state.quick_action = None
    
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    
    with st.chat_message("assistant"):
        model_response = support_function(
            user_prompt=prompt,
            chat_history=st.session_state.messages[:-1]  # Exclude current message
        )
        response = st.write_stream(response_generator(response=model_response))
    
    st.session_state.messages.append({"role": "assistant", "content": response})


if prompt := st.chat_input("How can I help you today?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.chat_message("assistant"):
        try:
            
            model_response = support_function(
                user_prompt=prompt,
                chat_history=st.session_state.messages[:-1] 
            )
            response = st.write_stream(response_generator(response=model_response))
            
        except Exception as e:
            response = f"Error: {str(e)}"
            st.error(response)
    
    
    st.session_state.messages.append({"role": "assistant", "content": response})


st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("Location: Bashorun Ojoo Road, Ibadan")
with col2:
    st.markdown("Phone: 08085017583")
with col3:
    st.markdown("Email: Ayorindesaheed2003@gmail.com")