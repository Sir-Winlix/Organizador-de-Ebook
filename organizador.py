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
        
        # Extraer el título, autor y género de los metadatos
        for item in book.get_metadata('DC', 'title'):
            metadata['title'] = item[0]
        
        for item in book.get_metadata('DC', 'creator'):
            metadata['author'] = item[0]
        
        # Obtener el género si está presente
        genre = book.get_metadata('DC', 'subject')
        if genre:
            metadata['genre'] = genre[0]
        
        return metadata
    except Exception as e:
        print(f"Error al leer {epub_path}: {e}")
        return {}

def organizar_epub(directory):
    # Crear carpeta de destino si no existe
    base_folder = os.path.join(directory, 'Organizados')
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    for filename in os.listdir(directory):
        if filename.endswith(".epub"):
            file_path = os.path.join(directory, filename)
            
            # Obtener metadatos del archivo
            metadatos = obtener_metadatos(file_path)
            
            # Crear carpeta por autor y género
            if 'author' in metadatos:
                author_folder = os.path.join(base_folder, limpiar_nombre(metadatos['author']))
                if not os.path.exists(author_folder):
                    os.makedirs(author_folder)
                
                # Crear carpeta por género
                if 'genre' in metadatos:
                    genre_folder = os.path.join(author_folder, limpiar_nombre(metadatos['genre']))
                    if not os.path.exists(genre_folder):
                        os.makedirs(genre_folder)
                    new_file_path = os.path.join(genre_folder, f"{limpiar_nombre(metadatos['title'])}.epub")
                else:
                    # Si no hay género, dejarlo en una carpeta "Sin_Género"
                    genre_folder = os.path.join(author_folder, 'Sin_Género')
                    if not os.path.exists(genre_folder):
                        os.makedirs(genre_folder)
                    new_file_path = os.path.join(genre_folder, f"{limpiar_nombre(metadatos['title'])}.epub")
                
                # Renombrar y mover el archivo
                print(f"Moviendo {file_path} a {new_file_path}")  # Registro para depuración
                shutil.move(file_path, new_file_path)

            else:
                # Si no hay autor, dejar en una carpeta común
                other_folder = os.path.join(base_folder, 'Sin_Autor')
                if not os.path.exists(other_folder):
                    os.makedirs(other_folder)
                
                # Si no hay género, mover a "Sin_Género"
                new_file_path = os.path.join(other_folder, filename)
                print(f"Moviendo {file_path} a {new_file_path}")  # Registro para depuración
                shutil.move(file_path, new_file_path)

if __name__ == "__main__":
    directory = input("Ingresa la ruta de la carpeta que contiene los archivos Epub: ")
    organizar_epub(directory)
    print("Los archivos Epub han sido organizados.")
