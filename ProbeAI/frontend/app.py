import base64
import io
import os
from PIL import Image
import requests
import streamlit as st
import pypdf

API_BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


script_dir = os.path.dirname(os.path.abspath(__file__))
possible_paths = [
    os.path.join(script_dir, "search.png"),
    os.path.join(script_dir, "frontend", "search.png"),
    "search.png",
    "frontend/search.png",
]

icon_path = None
for path in possible_paths:
    if os.path.exists(path):
        icon_path = path
        break

page_icon_img = None
try:
    if icon_path:
        page_icon_img = Image.open(icon_path)
    else:
        page_icon_img = "🔍"
except Exception:
    page_icon_img = "🔍"

st.set_page_config(
    page_title="ProbeAI Intelligence Hub",
    page_icon=page_icon_img,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

if "session_id" not in st.session_state:
    st.session_state["session_id"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "current_model" not in st.session_state:
    st.session_state["current_model"] = "llama3:latest"

with st.sidebar:
    st.markdown("### ⚙️ Research Settings")

    try:
        models_res = requests.get(
            f"{API_BASE_URL}/api/models", timeout=3
        ).json()
        available_models = models_res.get("models", ["llama3:latest"])
    except Exception:
        available_models = ["llama3:latest", "mistral:latest"]

    selected_model = st.selectbox(
        "Active LLM Model",
        options=available_models,
        index=(
            available_models.index(st.session_state["current_model"])
            if st.session_state["current_model"] in available_models
            else 0
        ),
    )
    st.session_state["current_model"] = selected_model

    use_web = st.toggle("🌐 Enable Web Grounding", value=True)
    temperature = st.slider(
        "🌡️ Creativity (Temperature)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
    )

    st.markdown("---")

    st.markdown("### 📁 Document Upload ")
    uploaded_file = st.file_uploader(
        "Attach PDF, TXT, or Code", type=["pdf", "txt", "py", "js", "md"]
    )

    document_context = ""
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/pdf":
                reader = pypdf.PdfReader(uploaded_file)
                extracted_pages = []
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_pages.append(text)
                document_context = "\n".join(extracted_pages)
            else:
                document_context = uploaded_file.read().decode(
                    "utf-8", errors="ignore"
                )

            st.success(
                f"Attached: {uploaded_file.name} ({len(document_context)} chars)"
            )
        except Exception as e:
            st.error(f"Error reading file: {e}")
            document_context = ""

    st.markdown("---")

    if st.button("➕ New Investigation", use_container_width=True):
        st.session_state["session_id"] = None
        st.session_state["messages"] = []
        st.rerun()

    if st.session_state["messages"]:
        chat_export = "\n\n".join(
            [
                f"**{m['role'].capitalize()}**: {m['content']}"
                for m in st.session_state["messages"]
            ]
        )
        st.download_button(
            label="📥 Export Investigation (.md)",
            data=chat_export,
            file_name="probeai_investigation.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.markdown("### 🗂️ Recent History")
    try:
        sessions_res = requests.get(
            f"{API_BASE_URL}/api/sessions", timeout=3
        ).json()
        sessions = sessions_res.get("sessions", [])

        if not sessions:
            st.caption("No past investigations found.")
        else:
            for sess in sessions:
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    if st.button(
                        sess["title"][:22] + "...",
                        key=f"sess_{sess['session_id']}",
                        use_container_width=True,
                    ):
                        detail_res = requests.get(
                            f"{API_BASE_URL}/api/sessions/{sess['session_id']}",
                            timeout=3,
                        ).json()
                        st.session_state["session_id"] = sess["session_id"]
                        st.session_state["messages"] = detail_res.get(
                            "messages", []
                        )
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"del_{sess['session_id']}"):
                        requests.delete(
                            f"{API_BASE_URL}/api/sessions/{sess['session_id']}"
                        )
                        if st.session_state["session_id"] == sess["session_id"]:
                            st.session_state["session_id"] = None
                            st.session_state["messages"] = []
                        st.rerun()
    except Exception:
        st.caption("Backend offline or unable to load history.")

    st.markdown("---")
    if st.button("Clear All Sessions", use_container_width=True):
        try:
            requests.delete(f"{API_BASE_URL}/api/sessions")
            st.session_state["session_id"] = None
            st.session_state["messages"] = []
            st.rerun()
        except Exception:
            pass


def get_image_base64(path):
    try:
        if path and os.path.exists(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception:
        return ""
    return ""


logo_b64 = get_image_base64(icon_path)

if logo_b64:
    st.markdown(
        f"""
        <div style='display: flex; align-items: center; gap: 12px; padding: 10px;'>
            <img src="data:image/png;base64,{logo_b64}" style='height: 42px; width: auto; object-fit: contain;' />
            <div>
                <h1 style='color: #ffffff; margin-bottom: 0px; font-size: 1.75rem; white-space: nowrap;'>ProbeAI Intelligence Hub</h1>
                <p style='color: #8a8d93; font-size: 14px; margin-top: 0px;'>Conversational AI Research & Web Intelligence Agent</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div style='text-align: center; padding: 10px;'>
            <h1 style='color: #ffffff; margin-bottom: 0px;'>🔍 ProbeAI Intelligence Hub</h1>
            <p style='color: #8a8d93; font-size: 14px;'>Conversational AI Research & Web Intelligence Agent</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask a research question or query documents...")

if user_input:
    st.session_state["messages"].append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        thought_container = st.empty()
        sources_container = st.empty()
        response_container = st.empty()

        full_response = ""
        planning_queries = []
        sources_list = []

        try:
            current_session = []
            for msg in st.session_state["messages"][:-1]:
                current_session.append(
                    {"role": msg["role"], "content": msg["content"]}
                )

            response = requests.post(
                f"{API_BASE_URL}/api/investigate",
                json={
                    "query": user_input,
                    "chat_history": current_session,
                    "use_web": use_web,
                    "model": selected_model,
                    "document_context": document_context,
                    "session_id": st.session_state["session_id"],
                    "temperature": temperature,
                },
                stream=True,
                timeout=300,
            )

            for line in response.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    try:
                        chunk_data = requests.compat.json.loads(decoded)
                        chunk_type = chunk_data.get("type")
                        chunk_val = chunk_data.get("data")

                        if chunk_type == "planning":
                            planning_queries = chunk_val
                            thought_content = thought_container.status(
                                "🧠 Agent Thought & Sub-Queries", expanded=True
                            )
                            with thought_content:
                                for idx, sq in enumerate(planning_queries):
                                    st.markdown(
                                        f"- **Step {idx+1} Search:** `{sq}`"
                                    )

                        elif chunk_type == "sources":
                            sources_list = chunk_val
                            if sources_list:
                                with sources_container.expander(
                                    "🌐 Grounded Web Sources", expanded=False
                                ):
                                    for s_idx, src in enumerate(sources_list):
                                        st.markdown(
                                            f"[{s_idx+1}] [{src['title']}]({src['url']})\n> _{src['snippet']}_"
                                        )

                        elif chunk_type == "token":
                            full_response += chunk_val
                            response_container.markdown(full_response + "▌")

                    except Exception:
                        pass

            response_container.markdown(full_response)

            st.session_state["messages"].append(
                {"role": "assistant", "content": full_response}
            )

            payload_to_save = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state["messages"]
            ]
            save_res = requests.post(
                f"{API_BASE_URL}/api/sessions",
                json={
                    "session_id": st.session_state["session_id"],
                    "title": user_input,
                    "payload": payload_to_save,
                },
            ).json()

            if not st.session_state["session_id"]:
                st.session_state["session_id"] = save_res.get("session_id")
                st.rerun()

        except Exception as e:
            error_msg = f"\n\n[Error communicating with backend: {e}]"
            full_response += error_msg
            response_container.markdown(full_response)