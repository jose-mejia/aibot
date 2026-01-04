from PIL import Image
import os
import sys

def convert_png_to_ico(source_png, dest_ico):
    if not os.path.exists(source_png):
        print(f"Erro: Arquivo {source_png} não encontrado.")
        return
    
    try:
        img = Image.open(source_png)
        # Salva como ICO contendo tamanhos padrão
        img.save(dest_ico, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
        print(f"Sucesso: {dest_ico} criado.")
    except Exception as e:
        print(f"Erro ao converter: {e}")

# Client Copier
convert_png_to_ico(
    r"c:\Users\josemejia\dev\python\aibot\backend\copy\client_copier\gui\src-tauri\icons\icon.png",
    r"c:\Users\josemejia\dev\python\aibot\backend\copy\client_copier\gui\src-tauri\icons\icon.ico"
)

# Master Sender
convert_png_to_ico(
    r"c:\Users\josemejia\dev\python\aibot\backend\copy\master_sender\gui\src-tauri\icons\icon.png",
    r"c:\Users\josemejia\dev\python\aibot\backend\copy\master_sender\gui\src-tauri\icons\icon.ico"
)
