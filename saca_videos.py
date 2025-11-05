"""
Download de Vídeos v2.0.5
Download de vídeos e áudio de 1000+ sites com redimensionamento para redes sociais

Autor: Rui Casaca
Data: Novembro 2025
Licença: MIT
"""

import os
import sys
import threading
import warnings
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
from pathlib import Path
import subprocess
import json


warnings.filterwarnings('ignore', category=DeprecationWarning)


def get_ffmpeg_path():
    """
    Retorna o caminho para o FFmpeg embarcado no executável ou no sistema
    """
    # Se estiver executando como executável (PyInstaller)
    if getattr(sys, 'frozen', False):
        # Executável: procurar na pasta do .exe
        base_path = sys._MEIPASS
        ffmpeg_bundled = os.path.join(base_path, 'ffmpeg_bin', 'ffmpeg.exe')
        if os.path.exists(ffmpeg_bundled):
            return ffmpeg_bundled
    else:
        # Modo desenvolvimento: procurar na pasta do projeto
        base_path = os.path.dirname(os.path.abspath(__file__))
        ffmpeg_local = os.path.join(base_path, 'ffmpeg_bin', 'ffmpeg.exe')
        if os.path.exists(ffmpeg_local):
            return ffmpeg_local
    
    # Fallback: usar FFmpeg do sistema (se instalado)
    return 'ffmpeg'


class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Descarregador de Vídeos v2.0.5 - por Rui Casaca")
        self.root.geometry("700x750")
        self.root.resizable(False, False)
        self.root.configure(bg='#f5f5f5')
        
        # Configurar estilo
        self.setup_styles()
        
        # Diretório de transferências
        self.downloads_folder = self.get_downloads_folder()
        
        # Variáveis
        self.is_downloading = False
        self.download_type = tk.StringVar(value='video')  # 'video' ou 'audio'
        self.last_downloaded_file = None  # Para rastrear último vídeo baixado
        self.last_video_title = None  # Para rastrear título do vídeo
        
        # Dimensões das redes sociais (largura x altura)
        self.social_media_specs = {
            'Instagram Feed (1:1)': {'width': 1080, 'height': 1080, 'aspect': '1:1'},
            'Instagram Story': {'width': 1080, 'height': 1920, 'aspect': '9:16'},
            'Instagram Reels': {'width': 1080, 'height': 1920, 'aspect': '9:16'},
            'TikTok': {'width': 1080, 'height': 1920, 'aspect': '9:16'},
            'YouTube Shorts': {'width': 1080, 'height': 1920, 'aspect': '9:16'},
            'Facebook Feed': {'width': 1280, 'height': 720, 'aspect': '16:9'},
            'Facebook Story': {'width': 1080, 'height': 1920, 'aspect': '9:16'},
            'Twitter/X': {'width': 1280, 'height': 720, 'aspect': '16:9'},
            'LinkedIn': {'width': 1280, 'height': 720, 'aspect': '16:9'},
            'YouTube (16:9)': {'width': 1920, 'height': 1080, 'aspect': '16:9'},
        }
        
        # Criar interface
        self.create_widgets()
        
    def setup_styles(self):
        """Configurar estilos da aplicação"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores de fundo
        style.configure('TFrame', background='#f5f5f5')
        style.configure('TLabelframe', background='#f5f5f5', borderwidth=2)
        style.configure('TLabelframe.Label', background='#f5f5f5', font=('Segoe UI', 10, 'bold'))
        
        # Labels
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), foreground='#1a5f7a', background='#f5f5f5')
        style.configure('Info.TLabel', font=('Segoe UI', 9), foreground='#666666', background='#f5f5f5')
        style.configure('Status.TLabel', font=('Segoe UI', 10), foreground='#333333', background='#ffffff')
        style.configure('Success.TLabel', font=('Segoe UI', 10, 'bold'), foreground='#2E8B57', background='#ffffff')
        style.configure('Error.TLabel', font=('Segoe UI', 10, 'bold'), foreground='#DB4545', background='#ffffff')
        
        # Radio buttons
        style.configure('TRadiobutton', background='#f5f5f5', font=('Segoe UI', 10))
        
        # Botões
        style.configure('Download.TButton', font=('Segoe UI', 12, 'bold'), padding=(20, 15))
        style.configure('Action.TButton', font=('Segoe UI', 9), padding=(10, 6))
        style.configure('Folder.TButton', font=('Segoe UI', 9, 'bold'), padding=(8, 6))
        
    def get_downloads_folder(self):
        """Obter pasta de transferências do sistema"""
        if os.name == 'nt':  # Windows
            return os.path.join(os.environ['USERPROFILE'], 'Downloads')
        else:  # Mac/Linux
            return os.path.join(os.environ['HOME'], 'Downloads')
    
    def create_widgets(self):
        """Criar elementos da interface"""
        # Frame principal com fundo
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título
        title_label = ttk.Label(
            header_frame,
            text="🎬 Download de Vídeos",
            style='Title.TLabel'
        )
        title_label.pack()
        
        # Subtítulo
        subtitle_label = ttk.Label(
            header_frame,
            text="Descarregue vídeos de YouTube, Facebook, Instagram, TikTok e muito mais",
            style='Info.TLabel'
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Frame da pasta de destino (com botão visível)
        dest_frame = ttk.Frame(main_frame)
        dest_frame.pack(fill=tk.X, pady=(0, 15))
        
        dest_label = ttk.Label(
            dest_frame,
            text=f"📁 Pasta de destino: {self.downloads_folder}",
            style='Info.TLabel',
            wraplength=450
        )
        dest_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botão para abrir pasta (sempre visível)
        self.open_folder_btn = ttk.Button(
            dest_frame,
            text="📂 Abrir Pasta",
            style='Folder.TButton',
            command=self.open_downloads_folder
        )
        self.open_folder_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Separador visual
        separator1 = ttk.Separator(main_frame, orient='horizontal')
        separator1.pack(fill=tk.X, pady=(0, 15))
        
        # Frame para URL
        url_frame = ttk.LabelFrame(main_frame, text=" 🔗 URL do Vídeo ", padding="15")
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Campo de entrada de URL
        self.url_entry = ttk.Entry(url_frame, font=('Segoe UI', 11))
        self.url_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        self.url_entry.bind('<Return>', lambda e: self.start_download())
        
        # Frame para botões de ação (Colar e Limpar)
        buttons_frame = ttk.Frame(url_frame)
        buttons_frame.pack(fill=tk.X)
        
        # Botão Colar
        paste_btn = ttk.Button(
            buttons_frame,
            text="📋 Colar",
            style='Action.TButton',
            command=self.paste_url
        )
        paste_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # Botão Limpar
        clear_btn = ttk.Button(
            buttons_frame,
            text="🗑️ Limpar",
            style='Action.TButton',
            command=self.clear_url
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Frame para escolha de tipo de download
        type_frame = ttk.LabelFrame(main_frame, text=" 🎯 Tipo de Download ", padding="15")
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Container para os radio buttons
        radio_container = ttk.Frame(type_frame)
        radio_container.pack()
        
        # Radio button para Vídeo
        video_radio = ttk.Radiobutton(
            radio_container,
            text="🎬 Vídeo (MP4)",
            variable=self.download_type,
            value='video'
        )
        video_radio.pack(side=tk.LEFT, padx=(0, 30))
        
        # Radio button para Áudio
        audio_radio = ttk.Radiobutton(
            radio_container,
            text="🎵 Apenas Áudio (M4A/WEBM)",
            variable=self.download_type,
            value='audio'
        )
        audio_radio.pack(side=tk.LEFT)
        
        # Nota informativa sobre formatos de áudio
        audio_note = ttk.Label(
            type_frame,
            text="ℹ️ O áudio será guardado em formato nativo (M4A ou WEBM), compatível com todos os players",
            style='Info.TLabel',
            wraplength=600
        )
        audio_note.pack(pady=(8, 0))
        
        # Frame para progresso
        progress_frame = ttk.LabelFrame(main_frame, text=" 📊 Estado do Download ", padding="15")
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Container com fundo branco para status
        status_container = tk.Frame(progress_frame, bg='#ffffff', relief=tk.FLAT, bd=1)
        status_container.pack(fill=tk.X, pady=(0, 10))
        
        # Label de status
        self.status_label = ttk.Label(
            status_container,
            text="Aguardando URL...",
            style='Status.TLabel'
        )
        self.status_label.pack(pady=10)
        
        # Container da barra de progresso moderna
        progress_container = tk.Frame(progress_frame, bg='#e0e0e0', relief=tk.FLAT, bd=0, height=35)
        progress_container.pack(fill=tk.X, pady=(0, 8))
        progress_container.pack_propagate(False)
        
        # Canvas para barra de progresso personalizada
        self.progress_canvas = tk.Canvas(
            progress_container,
            height=35,
            bg='#e0e0e0',
            highlightthickness=0
        )
        self.progress_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Retângulo de progresso (será atualizado dinamicamente)
        self.progress_rect = self.progress_canvas.create_rectangle(
            0, 0, 0, 35,
            fill='#1a8cff',
            outline=''
        )
        
        # Texto de percentagem sobreposto
        self.progress_text = self.progress_canvas.create_text(
            0, 17.5,
            text='0%',
            font=('Segoe UI', 10, 'bold'),
            fill='#333333'
        )
        
        # Label com informações adicionais (velocidade, tempo, tamanho)
        self.download_info_label = ttk.Label(
            progress_frame,
            text="",
            style='Info.TLabel',
            justify=tk.CENTER
        )
        self.download_info_label.pack()
        
        # Variável para rastrear progresso
        self.current_progress = 0
        
        # Separador visual
        separator2 = ttk.Separator(main_frame, orient='horizontal')
        separator2.pack(fill=tk.X, pady=(0, 15))
        
        # Frame para botões de ação (lado a lado)
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(5, 10))
        
        # Botão de Download (destaque - 70% da largura)
        self.download_btn = ttk.Button(
            buttons_frame,
            text="⬇️  Descarregar Vídeo",
            style='Download.TButton',
            command=self.start_download
        )
        self.download_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=5, padx=(0, 5))
        
        # Botão para redimensionar vídeo existente (30% da largura)
        self.resize_only_btn = ttk.Button(
            buttons_frame,
            text="Redimensionar apenas",
            style='Action.TButton',
            command=self.resize_existing_video
        )
        self.resize_only_btn.pack(side=tk.LEFT, fill=tk.Y, ipady=5)
    
    def update_progress_bar(self, percentage, info_text=""):
        """Atualizar barra de progresso moderna"""
        try:
            # Garantir que percentage está no intervalo correto
            percentage = max(0, min(100, percentage))
            
            # Atualizar retângulo de progresso
            canvas_width = self.progress_canvas.winfo_width()
            if canvas_width <= 1:  # Canvas ainda não foi renderizado
                canvas_width = 600
            
            progress_width = (canvas_width * percentage) / 100
            
            # Cores gradientes baseadas no progresso
            if percentage < 30:
                color = '#ff6b6b'  # Vermelho suave no início
            elif percentage < 70:
                color = '#ffa500'  # Laranja no meio
            else:
                color = '#2ecc71'  # Verde no final
            
            self.progress_canvas.coords(self.progress_rect, 0, 0, progress_width, 35)
            self.progress_canvas.itemconfig(self.progress_rect, fill=color)
            
            # Atualizar texto de percentagem (centralizado)
            self.progress_canvas.coords(self.progress_text, canvas_width / 2, 17.5)
            self.progress_canvas.itemconfig(
                self.progress_text,
                text=f'{int(percentage)}%',
                fill='#ffffff' if percentage > 10 else '#333333'
            )
            
            # Atualizar informações adicionais
            if info_text:
                self.download_info_label.config(text=info_text)
            
            # Forçar atualização do canvas
            self.progress_canvas.update_idletasks()
            
            self.current_progress = percentage
        except Exception as e:
            pass  # Ignorar erros de atualização visual
    
    def reset_progress_bar(self):
        """Resetar barra de progresso"""
        self.update_progress_bar(0, "")
        self.download_info_label.config(text="")
    
    def open_downloads_folder(self):
        """Abrir pasta de transferências no explorador de ficheiros"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.downloads_folder)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{self.downloads_folder}"')
            else:  # Linux
                os.system(f'xdg-open "{self.downloads_folder}"')
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a pasta: {str(e)}")
    
    def paste_url(self):
        """Colar URL do clipboard"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard_content)
            self.status_label.config(text="URL colado com sucesso!", style='Status.TLabel')
        except:
            self.status_label.config(text="Clipboard vazio ou inválido", style='Error.TLabel')
    
    def clear_url(self):
        """Limpar campo de URL"""
        self.url_entry.delete(0, tk.END)
        self.status_label.config(text="Campo limpo. Aguardando URL...", style='Status.TLabel')
        
    def validate_url(self, url):
        """Validar se a URL é válida"""
        if not url or url.strip() == '':
            return False, "Por favor, insira uma URL"
        
        if not url.startswith(('http://', 'https://')):
            return False, "URL deve começar com http:// ou https://"
        
        return True, ""
    
    def progress_hook(self, d):
        """Hook para acompanhar progresso do download"""
        if d['status'] == 'downloading':
            try:
                # Extrair dados de progresso
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                
                # Calcular percentagem
                if total > 0:
                    percentage = (downloaded / total) * 100
                else:
                    # Se não temos total, tentar usar campos alternativos
                    fragment_index = d.get('fragment_index', 0)
                    fragment_count = d.get('fragment_count', 0)
                    if fragment_count > 0:
                        percentage = (fragment_index / fragment_count) * 100
                    else:
                        percentage = 0
                
                # Formatar informações
                downloaded_mb = downloaded / (1024 * 1024)
                total_mb = total / (1024 * 1024) if total > 0 else 0
                speed_mb = speed / (1024 * 1024) if speed else 0
                
                # Criar texto de informação
                if total > 0:
                    info_text = f"📥 {downloaded_mb:.1f} MB / {total_mb:.1f} MB  |  "
                else:
                    info_text = f"📥 {downloaded_mb:.1f} MB  |  "
                
                if speed_mb > 0:
                    info_text += f"⚡ {speed_mb:.2f} MB/s  |  "
                
                if eta:
                    mins, secs = divmod(int(eta), 60)
                    info_text += f"⏱️ {mins}m {secs}s restantes"
                
                # Atualizar UI (usando lambda para evitar problemas de thread)
                self.root.after(0, lambda p=percentage, i=info_text: self.update_progress_bar(p, i))
                
                # Mensagem baseada no tipo de download
                download_msg = 'A descarregar áudio...' if self.download_type.get() == 'audio' else 'A descarregar vídeo...'
                self.root.after(0, lambda msg=download_msg: self.status_label.config(
                    text=msg,
                    style='Status.TLabel'
                ))
                
            except Exception as e:
                # Fallback para modo indeterminado
                download_msg = 'A descarregar áudio...' if self.download_type.get() == 'audio' else 'A descarregar vídeo...'
                self.root.after(0, lambda msg=download_msg: self.status_label.config(
                    text=msg,
                    style='Status.TLabel'
                ))
                
        elif d['status'] == 'finished':
            self.root.after(0, lambda: self.update_progress_bar(100, "✅ Download completo!"))
            
            # Mensagem de processamento baseada no tipo
            process_msg = 'Download concluído! A finalizar...' if self.download_type.get() == 'audio' else 'Download concluído! A processar ficheiro...'
            self.root.after(0, lambda msg=process_msg: self.status_label.config(
                text=msg,
                style='Status.TLabel'
            ))
    
    def download_video(self, url):
        """Realizar download do vídeo ou áudio"""
        try:
            # Verificar o tipo de download escolhido
            download_type = self.download_type.get()
            
            # Configurar formatos baseado na escolha
            if download_type == 'audio':
                # Apenas áudio em MP3
                format_options = ['bestaudio/best']
                file_extension = 'mp3'
            else:
                # Vídeo (configuração anterior)
                format_options = [
                    'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'best[ext=mp4]',
                    'best',
                ]
                file_extension = None  # Usa extensão automática
            
            video_title = None
            download_success = False
            last_error = None
            
            for i, format_str in enumerate(format_options):
                try:
                    # Configurar opções do yt-dlp
                    ydl_opts = {
                        'outtmpl': os.path.join(self.downloads_folder, '%(title)s.%(ext)s'),
                        'format': format_str,
                        'progress_hooks': [self.progress_hook],
                        'quiet': False,  # Permitir atualizações de progresso
                        'no_warnings': False,
                        'ignoreerrors': False,
                        'noprogress': False,  # Garantir que o progresso é reportado
                        'noplaylist': True,  # Baixar apenas o vídeo, não a playlist inteira
                    }
                    
                    # Se for áudio, tentar extrair sem ffmpeg (baixa em formato nativo)
                    # Não usamos postprocessors para evitar dependência do ffmpeg
                    if download_type == 'audio':
                        # Baixar o melhor áudio disponível (geralmente m4a, webm ou opus)
                        ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
                        # Nota: O arquivo será salvo no formato original (m4a, webm, etc)
                        # Não será convertido para MP3 sem ffmpeg
                    
                    # Iniciar download
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Extrair informações do vídeo primeiro (apenas na primeira tentativa)
                        if i == 0:
                            info = ydl.extract_info(url, download=False)
                            video_title = info.get('title', 'vídeo')
                            
                            self.status_label.config(
                                text=f"Vídeo encontrado: {video_title}",
                                style='Status.TLabel'
                            )
                        
                        # Fazer download
                        ydl.download([url])
                        
                        # Tentar encontrar o arquivo baixado
                        file_path = self.find_downloaded_file(video_title)
                        
                        download_success = True
                        break  # Se chegou aqui, download foi bem-sucedido
                        
                except yt_dlp.utils.DownloadError as e:
                    last_error = e
                    error_str = str(e).lower()
                    
                    # Se for erro de ffmpeg, tentar próximo formato
                    if 'ffmpeg' in error_str or 'merge' in error_str:
                        if i < len(format_options) - 1:
                            self.status_label.config(
                                text=f"A tentar formato alternativo ({i+2}/{len(format_options)})...",
                                style='Status.TLabel'
                            )
                            continue
                        else:
                            raise
                    else:
                        # Outros erros, lançar exceção
                        raise
                except Exception as e:
                    last_error = e
                    if i < len(format_options) - 1:
                        continue
                    else:
                        raise
            
            if not download_success:
                raise last_error if last_error else Exception("Falha ao descarregar com todos os formatos")
            
            # Garantir que a barra está em 100% ao terminar
            self.root.after(0, lambda: self.update_progress_bar(100, "✅ Download completo!"))
            
            # Sucesso - passar file_path também
            self.root.after(0, lambda: self.download_success(video_title, file_path))
            
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            if 'not a valid URL' in error_msg or 'Unsupported URL' in error_msg:
                self.root.after(0, self.download_error, 
                    "URL não suportado ou inválido. Verifique se o link está correto.")
            elif 'Video unavailable' in error_msg:
                self.root.after(0, self.download_error, 
                    "Vídeo não disponível ou privado.")
            else:
                self.root.after(0, self.download_error, 
                    f"Erro ao descarregar: {error_msg}")
        except Exception as e:
            self.root.after(0, self.download_error, 
                f"Erro inesperado: {str(e)}")
        finally:
            self.root.after(0, self.download_finished)
    
    def start_download(self):
        """Iniciar processo de download"""
        if self.is_downloading:
            messagebox.showwarning("Aviso", "Já existe um download em progresso!")
            return
        
        url = self.url_entry.get().strip()
        
        # Validar URL
        is_valid, error_msg = self.validate_url(url)
        if not is_valid:
            messagebox.showerror("Erro", error_msg)
            self.status_label.config(text=error_msg, style='Error.TLabel')
            return
        
        # Desativar botão e iniciar progresso
        self.is_downloading = True
        self.download_btn.config(state='disabled', text="⏳ A descarregar...")
        self.reset_progress_bar()
        self.status_label.config(text="A verificar URL e procurar vídeo...", style='Status.TLabel')
        
        # Teste rápido da barra de progresso
        self.root.after(100, lambda: self.update_progress_bar(5, "Iniciando..."))
        
        # Executar download em thread separada
        download_thread = threading.Thread(target=self.download_video, args=(url,), daemon=True)
        download_thread.start()
    
    def download_success(self, video_title, file_path=None):
        """Callback de sucesso"""
        # Garantir que a barra está em 100%
        self.update_progress_bar(100, "✅ Download completo!")
        
        # Armazenar informações do último download
        self.last_video_title = video_title
        self.last_downloaded_file = file_path
        
        # Se file_path não foi fornecido, tentar encontrar
        if not self.last_downloaded_file:
            self.last_downloaded_file = self.find_downloaded_file(video_title)
        
        # Debug: mostrar o caminho encontrado
        if self.last_downloaded_file:
            print(f"✓ Arquivo encontrado: {self.last_downloaded_file}")
        else:
            print(f"⚠ Aviso: Arquivo não encontrado para '{video_title}'")
        
        # Mensagem baseada no tipo de download
        download_type = self.download_type.get()
        type_text = "Áudio" if download_type == 'audio' else "Vídeo"
        file_type = "Áudio (M4A/WEBM)" if download_type == 'audio' else "MP4"
        icon = "🎵" if download_type == 'audio' else "🎬"
        
        self.status_label.config(
            text=f"✅ Download concluído com sucesso!",
            style='Success.TLabel'
        )
        
        messagebox.showinfo(
            "Sucesso",
            f"{type_text} descarregado com sucesso!\n\n"
            f"📁 Localização: {self.downloads_folder}\n"
            f"{icon} Título: {video_title}\n"
            f"📄 Formato: {file_type}"
        )
        
        # Se for vídeo E arquivo encontrado, perguntar sobre redimensionamento
        if download_type == 'video' and self.last_downloaded_file:
            self.ask_for_resize()
        
        # Finalizar processo
        self.download_finished()
    
    def download_error(self, error_msg):
        """Callback de erro"""
        self.reset_progress_bar()
        self.status_label.config(
            text=f"❌ Erro: {error_msg}",
            style='Error.TLabel'
        )
        messagebox.showerror("Erro no Download", error_msg)
    
    def download_finished(self):
        """Finalizar processo de download"""
        self.is_downloading = False
        self.download_btn.config(state='normal', text="⬇️  Descarregar Vídeo")
    
    def find_downloaded_file(self, video_title):
        """Encontrar o arquivo de vídeo baixado mais recente"""
        try:
            import glob
            import time
            
            # Procurar arquivos de vídeo na pasta de downloads
            video_extensions = ['.mp4', '.mkv', '.webm', '.avi', '.mov']
            files = []
            
            for ext in video_extensions:
                pattern = os.path.join(self.downloads_folder, f"*{ext}")
                files.extend(glob.glob(pattern))
            
            if not files:
                print(f"Nenhum arquivo de vídeo encontrado em: {self.downloads_folder}")
                return None
            
            # Obter arquivos modificados nos últimos 60 segundos
            current_time = time.time()
            recent_files = [
                f for f in files 
                if (current_time - os.path.getmtime(f)) < 60
            ]
            
            if not recent_files:
                print("Nenhum arquivo recente encontrado (últimos 60 segundos)")
                # Fallback: retornar o mais recente de todos
                recent_files = files
            
            # Retornar o arquivo mais recente
            latest_file = max(recent_files, key=os.path.getmtime)
            return latest_file
            
        except Exception as e:
            print(f"Erro ao encontrar arquivo: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def ask_for_resize(self):
        """Perguntar ao utilizador se quer redimensionar o vídeo"""
        response = messagebox.askyesno(
            "Redimensionar para Redes Sociais?",
            "Deseja redimensionar este vídeo para alguma rede social específica?\n\n"
            "Isto otimizará o vídeo para as dimensões exatas da plataforma escolhida."
        )
        
        if response:
            self.show_resize_dialog()
    
    def resize_existing_video(self):
        """Permitir redimensionar um vídeo existente sem download"""
        # Abrir diálogo para selecionar vídeo
        video_path = filedialog.askopenfilename(
            title="Selecione o vídeo para redimensionar",
            filetypes=[
                ("Vídeos", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm"),
                ("Todos os ficheiros", "*.*")
            ],
            initialdir=self.downloads_folder
        )
        
        # Se o utilizador cancelou
        if not video_path:
            return
        
        # Verificar se o ficheiro existe
        if not os.path.exists(video_path):
            messagebox.showerror(
                "Erro",
                "O ficheiro selecionado não existe!"
            )
            return
        
        # Guardar o caminho do vídeo e mostrar diálogo de redimensionamento
        self.last_downloaded_file = video_path
        # Extrair nome do ficheiro sem extensão para usar como título
        self.last_video_title = os.path.splitext(os.path.basename(video_path))[0]
        self.show_resize_dialog()
    
    def show_resize_dialog(self):
        """Mostrar diálogo simples e funcional para escolher rede social"""
        # Criar janela de diálogo
        resize_window = tk.Toplevel(self.root)
        resize_window.title("Redimensionar para Redes Sociais")
        resize_window.geometry("550x650")
        resize_window.resizable(False, False)
        resize_window.configure(bg='#f5f5f5')
        resize_window.transient(self.root)
        resize_window.grab_set()
        
        # Centralizar janela
        resize_window.update_idletasks()
        x = (resize_window.winfo_screenwidth() // 2) - (550 // 2)
        y = (resize_window.winfo_screenheight() // 2) - (650 // 2)
        resize_window.geometry(f'550x750+{x}+{y}')
        
        # Frame principal
        main_frame = tk.Frame(resize_window, bg='#ffffff', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="📱 Escolha a Plataforma",
            font=('Segoe UI', 16, 'bold'),
            bg='#ffffff',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = tk.Label(
            main_frame,
            text="Selecione para onde quer otimizar o vídeo:",
            font=('Segoe UI', 9),
            bg='#ffffff',
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Separador
        separator = tk.Frame(main_frame, height=2, bg='#ecf0f1')
        separator.pack(fill=tk.X, pady=(0, 15))
        
        # Variável para armazenar escolha
        selected_platform = tk.StringVar()
        
        # Frame para opções (com grid layout)
        options_frame = tk.Frame(main_frame, bg='#ffffff')
        options_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de plataformas organizada
        platforms_list = [
            ('📸 Instagram Feed (1:1)', 'Instagram Feed (1:1)', '1080×1080'),
            ('📸 Instagram Story', 'Instagram Story', '1080×1920'),
            ('📸 Instagram Reels', 'Instagram Reels', '1080×1920'),
            ('🎵 TikTok', 'TikTok', '1080×1920'),
            ('▶️ YouTube Shorts', 'YouTube Shorts', '1080×1920'),
            ('👥 Facebook Feed', 'Facebook Feed', '1920×1080'),
            ('👥 Facebook Story', 'Facebook Story', '1080×1920'),
            ('🐦 Twitter/X', 'Twitter/X', '1280×720'),
            ('💼 LinkedIn', 'LinkedIn', '1280×720'),
            ('🎬 YouTube', 'YouTube', '1920×1080'),
        ]
        
        # Criar radio buttons em lista simples
        for i, (display_name, value_name, dimensions) in enumerate(platforms_list):
            # Frame para cada opção
            option_container = tk.Frame(options_frame, bg='#ffffff')
            option_container.pack(fill=tk.X, pady=2)
            
            # Frame interno com borda
            option_frame = tk.Frame(
                option_container,
                bg='#f8f9fa',
                highlightbackground='#dee2e6',
                highlightthickness=1
            )
            option_frame.pack(fill=tk.X, padx=5)
            
            # Radio button
            rb = tk.Radiobutton(
                option_frame,
                text=display_name,
                variable=selected_platform,
                value=value_name,
                font=('Segoe UI', 10),
                bg='#f8f9fa',
                fg='#2c3e50',
                activebackground='#e9ecef',
                selectcolor='#ffffff',
                anchor='w',
                padx=10,
                pady=10
            )
            rb.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Label com dimensões
            dim_label = tk.Label(
                option_frame,
                text=dimensions,
                font=('Segoe UI', 9),
                bg='#f8f9fa',
                fg='#6c757d'
            )
            dim_label.pack(side=tk.RIGHT, padx=15)
            
            # Efeito hover
            def on_enter(e, frame=option_frame, rb=rb, lbl=dim_label):
                frame.config(bg='#e3f2fd', highlightbackground='#2196f3')
                rb.config(bg='#e3f2fd')
                lbl.config(bg='#e3f2fd')
            
            def on_leave(e, frame=option_frame, rb=rb, lbl=dim_label):
                frame.config(bg='#f8f9fa', highlightbackground='#dee2e6')
                rb.config(bg='#f8f9fa')
                lbl.config(bg='#f8f9fa')
            
            option_frame.bind('<Enter>', on_enter)
            option_frame.bind('<Leave>', on_leave)
            rb.bind('<Enter>', on_enter)
            rb.bind('<Leave>', on_leave)
            dim_label.bind('<Enter>', on_enter)
            dim_label.bind('<Leave>', on_leave)
        
        # Separador antes dos botões
        separator2 = tk.Frame(main_frame, height=2, bg='#ecf0f1')
        separator2.pack(fill=tk.X, pady=(15, 15))
        
        # Frame de botões
        buttons_frame = tk.Frame(main_frame, bg='#ffffff')
        buttons_frame.pack(fill=tk.X)
        
        def do_resize():
            platform = selected_platform.get()
            if not platform:
                messagebox.showwarning("Atenção", "Por favor, selecione uma plataforma!")
                return
            
            resize_window.destroy()
            self.resize_video(platform)
        
        # Botão Redimensionar
        resize_btn = tk.Button(
            buttons_frame,
            text="✂️  Redimensionar",
            font=('Segoe UI', 11, 'bold'),
            bg='#27ae60',
            fg='#ffffff',
            activebackground='#229954',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=12,
            command=do_resize
        )
        resize_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Hover para botão redimensionar
        def on_resize_enter(e):
            resize_btn.config(bg='#229954')
        
        def on_resize_leave(e):
            resize_btn.config(bg='#27ae60')
        
        resize_btn.bind('<Enter>', on_resize_enter)
        resize_btn.bind('<Leave>', on_resize_leave)
        
        # Botão Cancelar
        cancel_btn = tk.Button(
            buttons_frame,
            text="❌  Cancelar",
            font=('Segoe UI', 11),
            bg='#95a5a6',
            fg='#ffffff',
            activebackground='#7f8c8d',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            cursor='hand2',
            padx=20,
            pady=12,
            command=resize_window.destroy
        )
        cancel_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Hover para botão cancelar
        def on_cancel_enter(e):
            cancel_btn.config(bg='#7f8c8d')
        
        def on_cancel_leave(e):
            cancel_btn.config(bg='#95a5a6')
        
        cancel_btn.bind('<Enter>', on_cancel_enter)
        cancel_btn.bind('<Leave>', on_cancel_leave)
        
        # Atalho ESC
        resize_window.bind('<Escape>', lambda e: resize_window.destroy())
        
        # Focar na janela
        resize_window.focus_force()
    
    def resize_video(self, platform):
        """Redimensionar vídeo para a plataforma escolhida"""
        if not self.last_downloaded_file or not os.path.exists(self.last_downloaded_file):
            messagebox.showerror("Erro", "Arquivo de vídeo não encontrado!")
            return
        
        # Obter especificações
        specs = self.social_media_specs[platform]
        width = specs['width']
        height = specs['height']
        
        # Criar nome do arquivo de saída
        base_name = os.path.splitext(self.last_downloaded_file)[0]
        platform_safe = platform.replace('/', '-').replace(':', '').replace(' ', '_')
        output_file = f"{base_name}_{platform_safe}.mp4"
        
        # Atualizar UI
        self.status_label.config(
            text=f"🎬 Redimensionando para {platform}...",
            style='Status.TLabel'
        )
        self.reset_progress_bar()
        
        # Executar redimensionamento em thread separada
        thread = threading.Thread(
            target=self._do_resize_ffmpeg,
            args=(self.last_downloaded_file, output_file, width, height, platform),
            daemon=True
        )
        thread.start()
    
    def _do_resize_ffmpeg(self, input_file, output_file, width, height, platform):
        """Executar ffmpeg para redimensionar (usa ffmpeg embarcado ou do sistema)"""
        try:
            # Obter caminho do FFmpeg (embarcado ou sistema)
            ffmpeg_path = get_ffmpeg_path()
            
            # Comando ffmpeg para redimensionar mantendo aspect ratio
            command = [
                ffmpeg_path,  # Usar FFmpeg embarcado ou do sistema
                '-i', input_file,
                '-vf', f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2',
                '-c:a', 'copy',
                '-y',  # Sobrescrever sem perguntar
                output_file
            ]
            
            # Configurar para não mostrar janela do terminal no Windows
            startupinfo = None
            if os.name == 'nt':  # Windows
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            # Executar comando
            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            if process.returncode == 0:
                self.root.after(0, lambda: self.resize_success(output_file, platform))
            else:
                error_msg = process.stderr
                if 'not found' in error_msg.lower() or 'não encontrado' in error_msg.lower():
                    self.root.after(0, lambda: self.resize_error(
                        "FFmpeg não está instalado!\n\n"
                        "Para usar esta funcionalidade, instale o FFmpeg:\n"
                        "https://ffmpeg.org/download.html"
                    ))
                else:
                    self.root.after(0, lambda: self.resize_error(f"Erro ao redimensionar: {error_msg}"))
        
        except FileNotFoundError:
            self.root.after(0, lambda: self.resize_error(
                "FFmpeg não encontrado!\n\n"
                "Instale o FFmpeg para usar esta funcionalidade:\n"
                "https://ffmpeg.org/download.html"
            ))
        except Exception as e:
            self.root.after(0, lambda: self.resize_error(f"Erro inesperado: {str(e)}"))
    
    def resize_success(self, output_file, platform):
        """Callback quando redimensionamento é bem-sucedido"""
        self.status_label.config(
            text="✅ Vídeo redimensionado com sucesso!",
            style='Success.TLabel'
        )
        self.update_progress_bar(100, "✅ Redimensionamento completo!")
        
        messagebox.showinfo(
            "Sucesso!",
            f"Vídeo otimizado para {platform}!\n\n"
            f"📁 Localização: {output_file}\n\n"
            f"O vídeo está pronto para publicação!"
        )
    
    def resize_error(self, error_msg):
        """Callback quando redimensionamento falha"""
        self.status_label.config(
            text="❌ Erro no redimensionamento",
            style='Error.TLabel'
        )
        self.reset_progress_bar()
        
        messagebox.showerror("Erro", error_msg)


def main():
    """Função principal"""
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
