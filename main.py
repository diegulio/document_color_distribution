import streamlit as st
from app.processing import process_pdf, extract_images_from_pdf, calculate_pixel_distribution

def main():
    st.title("Analizador de Distribución de Píxeles en PDF")
    st.write("Sube un archivo PDF para calcular la distribución de píxeles de color, negros y blancos.")

    # File uploader
    uploaded_file = st.file_uploader("Elige un archivo PDF", type=["pdf"])
    
    if uploaded_file:
        # Save the uploaded file temporarily
        with open("archivo_subido.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.info("Procesando el archivo. Esto puede tomar algunos momentos...")

        try:
            # Step 1: Extracting images
            st.info("Paso 1: Extrayendo imágenes de las páginas del PDF...")
            images = extract_images_from_pdf("archivo_subido.pdf")
            total_pages = len(images)

            st.success(f"Paso 1 completo: Se extrajeron {total_pages} páginas.")

            # Step 2: Calculating pixels
            st.info("Paso 2: Calculando la distribución de píxeles...")
            progress_bar = st.progress(0)  # Initialize progress bar
            progress_text = st.empty()

            # Aggregate distributions
            total_distribution = {"color": 0, "black": 0, "white": 0}
            for i, image in enumerate(images):
                # Process each page
                distribution = calculate_pixel_distribution(image)

                # Update total distribution
                for key in total_distribution:
                    total_distribution[key] += distribution[key]

                # Update progress bar
                progress = (i + 1) / total_pages
                progress_bar.progress(progress)
                progress_text.text(f"Procesando página {i + 1} de {total_pages}...")

            # Average the distribution across all pages
            for key in total_distribution:
                total_distribution[key] /= total_pages

            # Clear progress bar and text
            progress_text.text("¡Cálculo completado!")
            progress_bar.empty()

            # Display the results
            st.success("Procesamiento completo.")
            st.subheader("Distribución de Píxeles:")
            st.write(f"**Color**: {total_distribution['color']:.2f}%")
            st.write(f"**Negros**: {total_distribution['black']:.2f}%")
            st.write(f"**Blancos**: {total_distribution['white']:.2f}%")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
