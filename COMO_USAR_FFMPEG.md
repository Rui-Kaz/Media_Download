# 🎬 Como Incluir FFmpeg no Executável

## 📋 Visão Geral

Para que o **redimensionamento de vídeos** funcione no executável standalone (sem precisar instalar FFmpeg no PC do utilizador), você precisa incluir o FFmpeg no build.

## 🚀 Passos Rápidos

### 1️⃣ Baixar FFmpeg Automaticamente

Execute o script fornecido:

```bash
python download_ffmpeg.py
```

Isto irá:
- ✅ Baixar FFmpeg essentials (~100 MB)
- ✅ Extrair os executáveis necessários
- ✅ Colocar em `ffmpeg_bin/`
- ✅ Preparar tudo para o build

### 2️⃣ Compilar com FFmpeg Incluído

Após o download, compile normalmente:

```bash
python build_exe.py
```

**OU** use o batch file:

```bash
compilar.bat
```

O batch file irá detectar automaticamente se FFmpeg está disponível e perguntar se quer baixá-lo.

## 📦 O que Acontece

### Com FFmpeg Incluído ✅
- Executável final: ~120-150 MB
- Redimensionamento funciona em **qualquer PC**
- Nenhuma dependência externa
- Experiência completa do utilizador

### Sem FFmpeg ⚠️
- Executável final: ~40-60 MB
- Redimensionamento **requer FFmpeg instalado** no PC
- Aplicação mostra mensagem de erro se FFmpeg não estiver disponível
- Download e áudio funcionam normalmente

## 🔧 Opção Manual

Se preferir baixar FFmpeg manualmente:

1. Acesse: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2. Baixe o arquivo ZIP
3. Extraia e copie estes arquivos para `ffmpeg_bin/`:
   - `ffmpeg.exe`
   - `ffprobe.exe`
4. Execute `python build_exe.py`

## 🎯 Estrutura de Pastas

```
PWEB/
├── saca_videos.py
├── build_exe.py
├── download_ffmpeg.py
├── compilar.bat
├── ffmpeg_bin/           ← Criar esta pasta
│   ├── ffmpeg.exe       ← Baixar estes arquivos
│   └── ffprobe.exe
└── dist/
    └── DescarregadorVideos.exe  ← Resultado final
```

## ❓ FAQ

**P: O download_ffmpeg.py é seguro?**  
R: Sim! Baixa diretamente do gyan.dev, uma fonte confiável e popular da comunidade FFmpeg.

**P: Preciso de internet para compilar?**  
R: Apenas para baixar FFmpeg (uma única vez). Depois pode compilar offline.

**P: Posso distribuir o .exe com FFmpeg?**  
R: Sim! FFmpeg usa licença GPL/LGPL que permite distribuição.

**P: E se já tiver FFmpeg instalado no sistema?**  
R: A aplicação primeiro tenta usar o FFmpeg embarcado, depois tenta o do sistema. É mais confiável embutir.

**P: Quanto aumenta o tamanho do executável?**  
R: Aproximadamente 80-100 MB adicionais.

## 📝 Notas Importantes

- ⚡ O download é feito **apenas uma vez**
- 🔄 Após baixar, todos os builds futuros incluirão FFmpeg automaticamente
- 🗑️ Para remover: delete a pasta `ffmpeg_bin/`
- 📦 O PyInstaller empacota tudo em um único .exe

## 💡 Recomendação

**Para distribuição pública**: SEMPRE inclua FFmpeg para melhor experiência do utilizador!
