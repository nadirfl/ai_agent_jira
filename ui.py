import streamlit as st
from tool_manager import load_tools
from llm import ask_ollama
from utils.fallback_handler import handle_fallback

tools = load_tools()
classify = tools["classify"]["run"]
extract = tools["extract"]["run"]
validate = tools["validate"]["run"]
create = tools["create"]["run"]
confirm = tools["confirm"]["run"]

st.title("JIRA Mail-Agent UI")

uploaded_file = st.file_uploader("Mail (.txt) hochladen", type="txt")

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    st.subheader("Mail-Inhalt")
    st.text(text)

    if st.button("Analysieren & Ticket vorbereiten"):
        with st.spinner("Klassifiziere..."):
            ticket_type = classify(text)
            st.write("Ticket-Typ: ", ticket_type)

        fields = extract(text)
        st.session_state.fields = fields
        st.write("Extrahierte Felder", fields)

        valid, errors, missing = validate(fields, ticket_type)
        st.session_state.ticket_type = ticket_type

        if not valid:
            st.error("Ticket unvollständig")
            for err in errors:
                st.write("-", err)
            
            for field in missing:
                action = st.radio(f"Feld '{field}' ergänzen?", ["Manuell", "LLM", "Überspringen"], key=field)
                if action == "Manuell":
                    user_input = st.text_input(f"Gib Wert für {field} ein:", key=f"{field}_input")
                    if user_input:
                        fields[field] = user_input
                elif action == "LLM":
                    suggestion = ask_ollama(f"Ergänze das Feld '{field}' basierend auf:\n{text}")
                    fields[field] = suggestion.strip()
        
        st.session_state.analysis_done = True
        
    if st.session_state.get("analysis_done", False):
        st.subheader("Ticket bereit zur Erstellung")

        if st.button("Ticket erstellen"):
            if "fields" in st.session_state and "ticket_type" in st.session_state:
                fields = st.session_state.fields
                ticket_type = st.session_state.ticket_type

                try:
                    result = create(fields, ticket_type)
                    ticket_key = result.get("key", "DEV-???")
                    message = confirm(fields, ticket_type, ticket_key)
                    st.success(message)

                    st.session_state.analysis_done = False
                    st.session_state.fields = None
                    st.session_state.ticket_type = None
                except Exception as e:
                    st.error("Fehler beim Erstellen.")
                    handle_fallback("streamlit_input", str(e), extracted_fields=fields)
            else:
                st.warning("Bitte analysiere zuerst eine Mail, bevor du ein Ticket erstellst.")