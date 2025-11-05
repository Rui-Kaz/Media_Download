"""
Script para baixar FFmpeg automaticamente
Este script baixa a versão standalone do FFmpeg para Windows
"""

import os
import sys
import urllib.request
import zipfile
import shutil

def download_with_progress(url, dest_path):
    """Baixar arquivo com barra de progresso"""
    try:
        with urllib.request.urlopen(url) as response:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 8192
            
            with open(dest_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        percent = downloaded * 100 / total_size
                        bar_length = 40
                        filled = int(bar_length * percent / 100)
                        bar = '█' * filled + '░' * (bar_length - filled)
                        mb_downloaded = downloaded / 1024 / 1024
                        mb_total = total_size / 1024 / 1024
                        print(f'\r[{bar}] {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)', end='', flush=True)
        print()  # Nova linha após completar
        return True
    except Exception as e:
        print(f"\n❌ Erro no download: {e}")
        return False

def download_ffmpeg():
    """
    Baixa FFmpeg essentials build para Windows
    """
    print("="*60)
    print("📥 BAIXANDO FFMPEG...")
    print("="*60)
    
    # URL do FFmpeg essentials build (versão leve)
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    
    # Criar pasta ffmpeg_bin se não existir
    ffmpeg_dir = os.path.join(os.path.dirname(__file__), 'ffmpeg_bin')
    os.makedirs(ffmpeg_dir, exist_ok=True)
    
    zip_path = os.path.join(ffmpeg_dir, 'ffmpeg.zip')
    
    print(f"\n📂 Pasta destino: {ffmpeg_dir}")
    print(f"🌐 Baixando de: {ffmpeg_url}")
    print(f"📦 Tamanho aproximado: ~100 MB")
    print("\n⏳ Aguarde, isto pode levar alguns minutos...\n")
    
    try:
        # Baixar arquivo
        if not download_with_progress(ffmpeg_url, zip_path):
            return False
        
        print('\n✅ Download completo!\n')
        
        # Extrair arquivos
        print("📦 Extraindo arquivos (aguarde)...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extrair mostrando progresso
            members = zip_ref.namelist()
            total = len(members)
            
            for i, member in enumerate(members, 1):
                zip_ref.extract(member, ffmpeg_dir)
                if i % 50 == 0 or i == total:  # Atualizar a cada 50 arquivos
                    percent = i * 100 / total
                    print(f'\rExtraindo: {percent:.0f}%', end='', flush=True)
            print()  # Nova linha
        
        # Encontrar pasta extraída e mover executáveis
        print("\n📋 Organizando arquivos...")
        extracted_folders = [f for f in os.listdir(ffmpeg_dir) 
                           if os.path.isdir(os.path.join(ffmpeg_dir, f)) and f.startswith('ffmpeg')]
        
        if extracted_folders:
            bin_folder = os.path.join(ffmpeg_dir, extracted_folders[0], 'bin')
            if os.path.exists(bin_folder):
                # Copiar apenas os executáveis necessários
                for file in ['ffmpeg.exe', 'ffprobe.exe']:
                    src = os.path.join(bin_folder, file)
                    if os.path.exists(src):
                        dst = os.path.join(ffmpeg_dir, file)
                        shutil.copy2(src, dst)
                        print(f"  ✓ {file}")
                
                # Limpar pasta temporária
                print("\n🧹 Limpando arquivos temporários...")
                shutil.rmtree(os.path.join(ffmpeg_dir, extracted_folders[0]), ignore_errors=True)
        
        # Remover arquivo zip
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        print("\n" + "="*60)
        print("✅ FFMPEG INSTALADO COM SUCESSO!")
        print("="*60)
        print(f"\n📁 Localização: {ffmpeg_dir}")
        print("\n💡 Arquivos prontos para build:")
        
        # Verificar arquivos
        for file in ['ffmpeg.exe', 'ffprobe.exe']:
            path = os.path.join(ffmpeg_dir, file)
            if os.path.exists(path):
                size_mb = os.path.getsize(path) / 1024 / 1024
                print(f"   ✓ {file} ({size_mb:.1f} MB)")
        
        print("\n🚀 Agora pode executar: python build_exe.py")
        print("   O executável incluirá FFmpeg embarcado!")
        print("\n" + "="*60)
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Download cancelado pelo utilizador.")
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return False
    except Exception as e:
        print(f"\n❌ Erro ao processar FFmpeg: {e}")
        print("\n⚠️  Você pode baixar manualmente de:")
        print("   https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
        print(f"   E extrair ffmpeg.exe e ffprobe.exe para: {ffmpeg_dir}")
        return False

if __name__ == '__main__':
    success = download_ffmpeg()
    sys.exit(0 if success else 1)
