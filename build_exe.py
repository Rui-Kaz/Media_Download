"""
Script para construir o executável do Descarregador de Vídeos
Execute este script para gerar o .exe standalone
"""

import PyInstaller.__main__
import os

# Diretório atual
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'saca_videos.py',                    # Script principal
    '--name=DescarregadorVideos',        # Nome do executável
    '--onefile',                         # Criar um único arquivo .exe
    '--windowed',                        # Não mostrar console (GUI apenas)
    '--icon=NONE',                       # Pode adicionar um ícone .ico aqui se tiver
    '--clean',                           # Limpar cache antes de compilar
    '--noconfirm',                       # Sobrescrever sem perguntar
    
    # Incluir módulos necessários
    '--hidden-import=yt_dlp',
    '--hidden-import=tkinter',
    '--hidden-import=threading',
    '--hidden-import=warnings',
    
    # Coletar dados do yt-dlp
    '--collect-all=yt_dlp',
    
    # Otimizações
    '--optimize=2',
])

print("\n" + "="*60)
print("✅ EXECUTÁVEL CRIADO COM SUCESSO!")
print("="*60)
print(f"\n📁 Localização: {os.path.join(current_dir, 'dist', 'DescarregadorVideos.exe')}")
print("\n💡 Pode copiar o arquivo .exe para qualquer computador Windows")
print("   e executá-lo sem precisar de Python instalado!")
print("\n" + "="*60)
