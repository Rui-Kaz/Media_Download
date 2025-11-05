"""
Script para construir o executável do Descarregador de Vídeos
Execute este script para gerar o .exe standalone
"""

import PyInstaller.__main__
import os
import sys

# Diretório atual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Verificar se FFmpeg está disponível
ffmpeg_bin_path = os.path.join(current_dir, 'ffmpeg_bin')
has_ffmpeg = os.path.exists(ffmpeg_bin_path) and any(
    f.endswith('.exe') for f in os.listdir(ffmpeg_bin_path)
)

if not has_ffmpeg:
    print("\n" + "="*60)
    print("⚠️  ATENÇÃO: FFmpeg não encontrado!")
    print("="*60)
    print("\n💡 Para incluir FFmpeg no executável (RECOMENDADO):")
    print("   1. Execute: python download_ffmpeg.py")
    print("   2. Aguarde o download completar")
    print("   3. Execute novamente este script\n")
    
    resposta = input("Deseja continuar sem FFmpeg? (s/N): ").strip().lower()
    if resposta != 's':
        print("\n❌ Build cancelado. Execute download_ffmpeg.py primeiro.")
        sys.exit(1)
    print("\n⚠️  Executável será criado SEM FFmpeg embarcado!")
    print("   O redimensionamento só funcionará se FFmpeg estiver instalado no sistema.\n")

# Preparar argumentos do PyInstaller
build_args = [
    'saca_videos.py',                    # Script principal
    '--name=DescarregadorVideos',        # Nome do executável
    '--onefile',                         # Criar um único arquivo .exe
    '--windowed',                        # Não mostrar console (GUI apenas)
    '--icon=NONE',                       # Pode adicionar um ícone .ico aqui se tiver
    '--clean',                           # Limpar cache antes de compilar
    '--noconfirm',                       # Sobrescrever sem perguntar
    '--version-file=version_info.txt',   # Informações de versão e autor
    
    # Incluir módulos necessários
    '--hidden-import=yt_dlp',
    '--hidden-import=tkinter',
    '--hidden-import=threading',
    '--hidden-import=warnings',
    
    # Coletar dados do yt-dlp
    '--collect-all=yt_dlp',
    
    # Otimizações
    '--optimize=2',
]

# Se FFmpeg disponível, incluir no executável
if has_ffmpeg:
    print(f"\n✅ FFmpeg encontrado em: {ffmpeg_bin_path}")
    print("📦 Incluindo FFmpeg no executável...\n")
    build_args.append(f'--add-data={ffmpeg_bin_path};ffmpeg_bin')

# Executar PyInstaller
PyInstaller.__main__.run(build_args)

print("\n" + "="*60)
print("✅ EXECUTÁVEL CRIADO COM SUCESSO!")
print("="*60)
print(f"\n📁 Localização: {os.path.join(current_dir, 'dist', 'DescarregadorVideos.exe')}")

if has_ffmpeg:
    print("\n✅ FFmpeg INCLUÍDO no executável!")
    print("   → Redimensionamento funcionará em qualquer PC!")
else:
    print("\n⚠️  FFmpeg NÃO incluído")
    print("   → Redimensionamento requer FFmpeg instalado no sistema")

print("\n💡 Pode copiar o arquivo .exe para qualquer computador Windows")
print("   e executá-lo sem precisar de Python instalado!")
print("\n" + "="*60)
