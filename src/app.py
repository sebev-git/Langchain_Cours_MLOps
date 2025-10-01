import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  

if "api_session" not in st.session_state:
    st.session_state.api_session = requests.Session()

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# === Auth ===
st.sidebar.header("🔑 Authentication")
choice = st.sidebar.radio("Action:", ["Login", "Register"])

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if choice == "Register":
    if st.sidebar.button("Create account"):
        res = st.session_state.api_session.post(
            f"{API_URL}/register",
            json={"username": username, "password": password}
        )
        if res.status_code == 200:
            st.success("✅ Account created, please login now")
        else:
            st.error(res.json()["detail"])

if choice == "Login":
    if st.sidebar.button("Login"):
        res = st.session_state.api_session.post(
            f"{API_URL}/login",
            json={"username": username, "password": password}
        )
        if res.status_code == 200:
            data = res.json()
            if "user_id" in data:
                st.session_state.user_id = data["user_id"]
                st.success(f"✅ Logged in as {st.session_state.user_id}")
            else:
                st.error("Unexpected API response")
        else:
            st.error(res.json().get("detail", "Login error"))

# === Main App ===
st.title("📚 DocuAgent - Document Analysis")

if st.session_state.user_id:
    st.subheader(f"Welcome {st.session_state.user_id}!")

    # === Upload file ===
    st.header("📤 Upload a document")
    uploaded_file = st.file_uploader("Choose a file (PDF, TXT, MD)", type=["pdf", "txt", "md"])
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        res = st.session_state.api_session.post(
            f"{API_URL}/upload_file?user_id={st.session_state.user_id}", 
            files=files
        )
        if res.status_code == 200:
            st.success(f"✅ File {uploaded_file.name} uploaded")
            st.json(res.json())
        else:
            st.error(res.json()["detail"])

    # === Tabs for actions ===
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📝 Summary", "🏷️ Classification", "🌍 Translation", "🤖 Agent", "🗂️ Memory", "💬 Free Chat"]
    )

    # Summary
    with tab1:
        st.subheader("Document Summary")
        if st.button("Generate summary"):
            res = st.session_state.api_session.post(f"{API_URL}/doc_summary")
            data = res.json()
            if res.status_code == 200 and "summary" in data:
                st.success("✅ Summary generated")
                st.write(data["summary"])   
            else:
                st.error(data.get("detail", "Unexpected error"))
                st.json(data)

    # Classification
    with tab2:
        st.subheader("Document Classification")
        if st.button("Classify document"):
            res = st.session_state.api_session.post(f"{API_URL}/doc_classify")
            data = res.json()
            if res.status_code == 200 and "category" in data:
                st.success("✅ Classification successful")
                st.markdown(f"**Category:** {data['category']}")
                st.markdown(f"**Confidence:** {round(data['confidence']*100, 2)} %")
            else:
                st.error(data.get("detail", "Unexpected error"))
                st.json(data)  

    # Translation
    with tab3:
        st.subheader("Summary Translation")
        if st.button("Translate"):
            res = st.session_state.api_session.post(f"{API_URL}/doc_translate?user_id={st.session_state.user_id}") 
            data = res.json()
            if res.status_code == 200:
                st.success("✅ Translation generated")
                st.write(data["translated"])
            else:
                st.error(data.get("detail", "Unexpected error"))
                st.json(data)  

    # Agent
    with tab4:
        st.subheader("Ask the Agent")
        query = st.text_area("Ask your question")
        if st.button("Send"):
            res = st.session_state.api_session.post(f"{API_URL}/agent", json={"query": query})
            data = res.json()
            if res.status_code == 200:
                if data.get("response"):
                    st.success("✅ Agent response")
                    st.write(data["response"])
                else:
                    st.warning("⚠️ No result found in the document.")
            else:
                st.error(data.get("detail", "Unexpected error"))
                st.json(data)
    
    # Memory
    with tab5:
        st.subheader("🗂️ Memory History")
        if st.button("Show history"):
            res = st.session_state.api_session.get(f"{API_URL}/history")
            data = res.json()
            if res.status_code == 200:
                st.success(f"History of {data['user_id']}")
                for msg in data["messages"]:
                    role = msg["type"]
                    content = msg["content"]
                    st.markdown(f"**{role}:** {content}")
            else:
                st.error(data.get("detail", "Unexpected error"))
                st.json(data)

    # Free Chat
    with tab6:
        st.subheader("💬 Free conversation with the bot")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        query = st.text_area("Your message")
        if st.button("Send to chat"):
            res = st.session_state.api_session.post(f"{API_URL}/chat", json={"query": query})
            data = res.json()
            if res.status_code == 200:
                response = data.get("response", "")
                st.session_state.chat_history.append(("👤", query))
                st.session_state.chat_history.append(("🤖", response))
                st.session_state.chat_input = ""
                st.rerun()

        # Local history display
        if st.session_state.chat_history:
            st.subheader("Conversation History")
            for role, content in st.session_state.chat_history:
                st.markdown(f"**{role}**: {content}")

else:
    st.info("🔒 Please log in or register to use the app.")