from datetime import datetime
import os
import streamlit as st

from attachments import validate_upload, save_upload
from db_core import add_material, list_materials


def render_materials_admin(default_subject=None):
    st.markdown('<div class="materials-card">', unsafe_allow_html=True)
    st.markdown("### Base de conteúdos dos professores")
    st.caption("Alimente o sistema com slides, listas, provas, PDFs, roteiros e materiais internos.")

    with st.form("materials_form"):
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Título do material")
            subjects = ["Matemática", "Física", "Metodologia Científica", "Documentos Acadêmicos"]
            idx = subjects.index(default_subject) if default_subject in subjects else 0
            subject = st.selectbox("Área", subjects, index=idx)

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
                    file_path, file_name, file_type = save_upload(uploaded_file)

                    content_parts = []
                    if description.strip():
                        content_parts.append(description.strip())
                    if tags.strip():
                        content_parts.append(f"Tags: {tags.strip()}")
                    content_parts.append(f"Tipo do arquivo: {file_type}")
                    content = "\n\n".join(content_parts)

                    add_material(
                        title=title.strip(),
                        subject=subject,
                        teacher_name=teacher_name.strip() or None,
                        content=content,
                        file_name=file_name,
                        file_path=file_path,
                    )

                    st.success("Material salvo com sucesso.")
                    st.rerun()

    rows = list_materials(subject=default_subject)

    if rows:
        st.markdown("#### Materiais já cadastrados")
        for row in rows:
            st.markdown(f"**{row['title']}**")

            meta = [row["subject"]]
            if row.get("teacher_name"):
                meta.append(row["teacher_name"])
            if row.get("file_name"):
                meta.append(row["file_name"])

            st.caption(" • ".join(meta))

            st.write(row.get("content") or "Sem descrição.")

            if row.get("file_path"):
                st.caption(f"Caminho: {row['file_path']}")

            st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)
