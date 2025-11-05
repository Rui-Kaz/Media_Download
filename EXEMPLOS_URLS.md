# 📋 Exemplos de URLs Suportados

## ✅ URLs que funcionam corretamente

### YouTube

#### Vídeo Individual
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```
**Comportamento**: Baixa apenas este vídeo ✅

#### Vídeo com Playlist (CORRIGIDO v2.0.1)
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf
```
**Comportamento**: Baixa **apenas o vídeo** `dQw4w9WgXcQ`, **ignora a playlist** ✅

**Antes da v2.0.1**: Tentava baixar toda a playlist ❌  
**Depois da v2.0.1**: Baixa apenas o vídeo específico ✅

#### Vídeo do YouTube Shorts
```
https://www.youtube.com/shorts/abc123xyz
```
**Comportamento**: Baixa o Short ✅

#### URL Encurtado
```
https://youtu.be/dQw4w9WgXcQ
```
**Comportamento**: Baixa o vídeo ✅

---

### Outras Plataformas

#### Instagram
```
https://www.instagram.com/reel/ABC123xyz/
https://www.instagram.com/p/ABC123xyz/
```
**Comportamento**: Baixa o Reel ou Post ✅

#### TikTok
```
https://www.tiktok.com/@username/video/1234567890123456789
https://vt.tiktok.com/ZSFxyz123/
```
**Comportamento**: Baixa o vídeo ✅

#### Facebook
```
https://www.facebook.com/watch/?v=1234567890
https://fb.watch/abc123/
```
**Comportamento**: Baixa o vídeo ✅

#### Twitter/X
```
https://twitter.com/username/status/1234567890
https://x.com/username/status/1234567890
```
**Comportamento**: Baixa o vídeo ✅

---

## 🎯 Configuração Técnica

A opção `noplaylist: True` foi adicionada ao yt-dlp para garantir que apenas o vídeo específico seja baixado:

```python
ydl_opts = {
    'outtmpl': os.path.join(self.downloads_folder, '%(title)s.%(ext)s'),
    'format': format_str,
    'progress_hooks': [self.progress_hook],
    'quiet': False,
    'no_warnings': False,
    'ignoreerrors': False,
    'noprogress': False,
    'noplaylist': True,  # ← NOVA OPÇÃO
}
```

---

## 💡 Notas Importantes

1. **Playlists Completas**: Se quiser baixar uma playlist inteira, isso requereria uma versão diferente da aplicação com `noplaylist: False`

2. **URLs Diretos vs Playlists**: 
   - Se colar um URL de playlist direta (ex: `youtube.com/playlist?list=...`), a opção `noplaylist: True` impedirá o download
   - Se colar um URL de vídeo com `&list=`, apenas o vídeo será baixado

3. **Compatibilidade**: Funciona com mais de 1000 sites suportados pelo yt-dlp

---

## 🔧 Como Testar

1. Abra a aplicação
2. Cole um URL do YouTube com `&list=` no final
3. Clique em "Descarregar Vídeo"
4. Verifique que apenas **1 vídeo** é baixado ✅

**Exemplo de teste**:
```
https://www.youtube.com/watch?v=jNQXAC9IVRw&list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf
```

Resultado esperado: Baixa apenas "Me at the zoo" (primeiro vídeo do YouTube), não a playlist inteira.
