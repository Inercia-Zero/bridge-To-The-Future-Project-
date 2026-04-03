from datetime import datetime
import streamlit as st

from attachments import validate_upload, save_upload
from database import save_material_record, list_materials

def render_materials_admin():
    st.markdown('<div class="materials-box">', unsafe_allow_html=True)
    st.markdown('<div class="materials-title">Base de conteúdos dos professores</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="materials-sub">Alimente o sistema com slides, listas, provas, PDFs, roteiros e materiais internos.</div>',
        unsafe_allow_html=True,
    )

    with st.form("materials_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Título do material")
            subject = st.selectbox("Área", ["Matemática", "Física", "Metodologia Científica", "Documentos Acadêmicos"])
        with col2:
            teacher_name = st.text_input("Professor(a)")
            tags = st.text_input("Tags (separadas por vírgula)")

        description = st.text_area("Descrição")
        uploaded_file = st.file_uploader(
            "Envie PDF, imagem ou TXT",
            type=["pdf", "png", "jpg", "jpeg", "webp", "txt"],
        )

        submitted = st.form_submit_button("Salvar material")

        if submitted:
            if not title.strip():
                st.error("Digite um título.")
            elif uploaded_file is None:
                st.error("Envie um arquivo.")
            else:
                error = validate_upload(uploaded_file)
                if error:
                    st.error(error)
                else:
                    file_path, _, file_type = save_upload(uploaded_file)
                    save_material_record(
                        title=title.strip(),
                        subject=subject,
                        teacher_name=teacher_name.strip(),
                        description=description.strip(),
                        file_path=file_path,
                        file_type=file_type,
                        tags=tags.strip(),
                        uploaded_at=datetime.utcnow().isoformat(),
                    )
                    st.success("Material salvo com sucesso.")
                    st.rerun()

    rows = list_materials()
    if rows:
        st.markdown("### Materiais já cadastrados")
        for row in rows:
            st.markdown(
                f"""
                <div class="mentor-card">
                    <div class="mentor-name">{row['title']}</div>
                    <div class="mentor-desc"><b>Área:</b> {row['subject']} | <b>Professor:</b> {row['teacher_name'] or 'Não informado'}</div>
                    <div class="mentor-desc" style="margin-top:8px;">{row['description'] or 'Sem descrição.'}</div>
                    <div class="mentor-desc" style="margin-top:8px;"><b>Tipo:</b> {row['file_type']} | <b>Tags:</b> {row['tags'] or '-'}</div>
                    <div class="mentor-desc" style="margin-top:6px;"><b>Enviado em:</b> {row['uploaded_at']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)
