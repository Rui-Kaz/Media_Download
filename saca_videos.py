import os
import sys
import threading
import warnings
import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
from pathlib import Path

# Suprimir avisos de deprecação (você já está usando Python 3.14)
warnings.filterwarnings('ignore', category=DeprecationWarning)


class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Descarregador de Vídeos")
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
        
        # Botão de Download (destaque)
        self.download_btn = ttk.Button(
            main_frame,
            text="⬇️  Descarregar Vídeo",
            style='Download.TButton',
            command=self.start_download
        )
        self.download_btn.pack(fill=tk.X, pady=(5, 0), ipady=5)
    
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
            
            # Sucesso
            self.root.after(0, self.download_success, video_title)
            
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
    
    def download_success(self, video_title):
        """Callback de sucesso"""
        # Garantir que a barra está em 100%
        self.update_progress_bar(100, "✅ Download completo!")
        
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


def main():
    """Função principal"""
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
