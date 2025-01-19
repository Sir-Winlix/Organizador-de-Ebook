import os
import shutil
from ebooklib import epub
import re

def limpiar_nombre(nombre):
    # Reemplaza caracteres no válidos en nombres de archivo y carpetas
    return re.sub(r'[\\/*?:"<>|]', '_', nombre)

def obtener_metadatos(epub_path):
    try:
        book = epub.read_epub(epub_path)
        metadata = {}
        
        # Extraer el título y autor de los metadatos
        for item in book.get_metadata('DC', 'title'):
            metadata['title'] = item[0]
        
        for item in book.get_metadata('DC', 'creator'):
            metadata['author'] = item[0]
        
        return metadata
    except Exception as e:
        print(f"Error al leer {epub_path}: {e}")
        return {}

def organizar_epub(directory):
    # Crear carpetas para organizar por autor
    if not os.path.exists('Organizados'):
        os.makedirs('Organizados')

    for filename in os.listdir(directory):
        if filename.endswith(".epub"):
            file_path = os.path.join(directory, filename)
            
            # Obtener metadatos del archivo
            metadatos = obtener_metadatos(file_path)
            
            if 'author' in metadatos:
                author_folder = os.path.join('Organizados', limpiar_nombre(metadatos['author']))
                if not os.path.exists(author_folder):
                    os.makedirs(author_folder)

                # Normalizar el nombre del archivo
                title = limpiar_nombre(metadatos['title'])
                new_file_path = os.path.join(author_folder, f"{title}.epub")
                
                # Renombrar y mover el archivo
                shutil.move(file_path, new_file_path)

            else:
                # Si no hay autor, dejar en una carpeta común
                other_folder = os.path.join('Organizados', 'Sin_Autor')
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
                
                shutil.move(file_path, os.path.join(other_folder, filename))

if __name__ == "__main__":
    directory = input("Ingresa la ruta de la carpeta que contiene los archivos Epub: ")
    organizar_epub(directory)
    print("Los archivos Epub han sido organizados.")
