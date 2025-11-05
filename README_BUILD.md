# 🎬 Descarregador de Vídeos - Guia de Compilação

## 📋 Como Criar o Executável (.exe)

### Passo 1️⃣: Instalar Dependências
```bash
pip install pyinstaller yt-dlp
```

### Passo 2️⃣: Executar o Script de Compilação
```bash
python build_exe.py
```

### Passo 3️⃣: Localizar o Executável
Após a compilação, o executável estará em:
```
h:\PWEB\dist\DescarregadorVideos.exe
```

---

## 📦 Distribuição

O arquivo `.exe` gerado é **totalmente standalone**:
- ✅ Não requer Python instalado
- ✅ Não requer bibliotecas externas
- ✅ Inclui todas as dependências (yt-dlp, tkinter, etc.)
- ✅ Funciona em qualquer Windows (7, 8, 10, 11)
- ✅ Pode ser copiado para qualquer computador

---

## 🎯 Funcionalidades do Programa

### Download de Vídeos
- Suporta: YouTube, Facebook, Instagram, TikTok, Twitter e muitos outros
- Formato: MP4 (melhor qualidade disponível)

### Download de Áudio
- Extrai apenas o áudio do vídeo
- Formatos: M4A ou WEBM (compatíveis com todos os players)

### Interface Moderna
- Barra de progresso com percentagem em tempo real
- Informações de velocidade e tempo restante
- Botão para abrir pasta de downloads
- Design intuitivo e limpo

---

## 🔧 Opções Avançadas de Compilação

### Adicionar Ícone Personalizado
1. Coloque um arquivo `.ico` na pasta do projeto
2. Edite `build_exe.py` e altere a linha:
   ```python
   '--icon=NONE',
   ```
   para:
   ```python
   '--icon=meu_icone.ico',
   ```

### Reduzir Tamanho do Executável
Se o .exe ficar muito grande, pode usar:
```python
'--exclude-module=matplotlib',
'--exclude-module=numpy',
'--exclude-module=pandas',
```

### Mostrar Console (para debug)
Remova ou comente a linha:
```python
'--windowed',
```

---

## 📝 Notas Importantes

### Antivírus
Alguns antivírus podem marcar o .exe como suspeito (falso positivo).
Isso é normal com programas Python compilados. Pode adicionar exceção no antivírus.

### Tamanho do Arquivo
O executável terá aproximadamente 30-50 MB devido às bibliotecas incluídas.

### Atualizações
Para atualizar o programa:
1. Modifique o código em `saca_videos.py`
2. Execute novamente `python build_exe.py`
3. Distribua o novo .exe

---

## 🆘 Resolução de Problemas

### Erro: "ModuleNotFoundError"
Instale as dependências:
```bash
pip install yt-dlp pyinstaller
```

### Erro ao executar o .exe
Execute o build sem `--windowed` para ver mensagens de erro:
```bash
python build_exe.py
# (remova '--windowed' do script)
```

### .exe muito lento para iniciar
É normal. A primeira vez que executa pode demorar 5-10 segundos.

---

## 📧 Suporte

Para problemas ou dúvidas, verifique:
- Documentação do PyInstaller: https://pyinstaller.org
- Documentação do yt-dlp: https://github.com/yt-dlp/yt-dlp

---

**Criado com ❤️ usando Python + Tkinter + yt-dlp**
