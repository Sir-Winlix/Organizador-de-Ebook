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
        title = book.get_metadata('DC', 'title')
        if title:
            metadata['title'] = title[0][0]
        
        author = book.get_metadata('DC', 'creator')
        if author:
            metadata['author'] = author[0][0]
        
        # Obtener el género si está presente
        genre = book.get_metadata('DC', 'subject')
        if genre:
            metadata['genre'] = genre[0][0]
        
        return metadata
    except Exception as e:
        print(f"Error al leer {epub_path}: {e}")
        return {}

def organizar_epub(directory, destino_base, mostrar_progreso=False):
    # Crear carpeta de destino si no existe
    if not os.path.exists(destino_base):
        os.makedirs(destino_base)
    
    total_archivos = sum([len(files) for r, d, files in os.walk(directory) if any(f.endswith('.epub') for f in files)])
    archivos_procesados = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.epub'):
                epub_path = os.path.join(root, file)
                metadata = obtener_metadatos(epub_path)
                
                if metadata:
                    title = limpiar_nombre(metadata.get('title', 'Desconocido'))
                    author = limpiar_nombre(metadata.get('author', 'Desconocido'))
                    genre = limpiar_nombre(metadata.get('genre', 'Desconocido'))
                    
                    # Crear carpetas basadas en los metadatos
                    genre_folder = os.path.join(destino_base, genre)
                    author_folder = os.path.join(genre_folder, author)
                    if not os.path.exists(author_folder):
                        os.makedirs(author_folder)
                    
                    # Mover el archivo a la carpeta correspondiente
                    destino = os.path.join(author_folder, f"{title}.epub")
                    shutil.move(epub_path, destino)
                    archivos_procesados += 1
                    if mostrar_progreso:
                        print(f"Movido: {epub_path} -> {destino}")
                        print(f"Progreso: {archivos_procesados}/{total_archivos} archivos procesados")

if __name__ == "__main__":
    directory = input("Ingresa la ruta de la carpeta que contiene los archivos Epub: ")
    destino_base = input("Ingresa la ruta de la carpeta de destino: ")
    mostrar_progreso = input("¿Deseas ver el progreso? (s/n): ").lower() == 's'
    organizar_epub(directory, destino_base, mostrar_progreso)
    print("Los archivos Epub han sido organizados.")