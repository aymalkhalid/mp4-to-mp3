import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from moviepy import VideoFileClip
import os
import sys
import threading
from pathlib import Path


class MP4ToMP3Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("MP4 to MP3 Converter")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.conversion_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="MP4 to MP3 Converter", 
                               font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input file selection
        ttk.Label(main_frame, text="Input MP4 File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        input_entry = ttk.Entry(main_frame, textvariable=self.input_file, width=50)
        input_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="Browse", 
                  command=self.browse_input_file).grid(row=1, column=2, pady=5)
        
        # Output file selection
        ttk.Label(main_frame, text="Output MP3 File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(main_frame, textvariable=self.output_file, width=50)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="Browse", 
                  command=self.browse_output_file).grid(row=2, column=2, pady=5)
        
        # Convert button
        self.convert_button = ttk.Button(main_frame, text="Convert to MP3", 
                                        command=self.start_conversion)
        self.convert_button.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to convert", foreground="green")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # File info frame
        info_frame = ttk.LabelFrame(main_frame, text="File Information", padding="10")
        info_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 0))
        info_frame.columnconfigure(1, weight=1)
        
        self.info_text = tk.Text(info_frame, height=8, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        info_frame.rowconfigure(0, weight=1)
        
    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select MP4 file",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Auto-generate output filename in Documents folder for better compatibility
            input_path = Path(filename)
            documents_dir = os.path.join(os.path.expanduser("~"), "Documents")
            output_filename = input_path.stem + '.mp3'
            output_path = os.path.join(documents_dir, output_filename)
            self.output_file.set(output_path)
            self.show_file_info(filename)
            
    def browse_output_file(self):
        # Default to user's Documents folder for better compatibility
        import os
        default_dir = os.path.join(os.path.expanduser("~"), "Documents")
        
        filename = filedialog.asksaveasfilename(
            title="Save MP3 file as",
            defaultextension=".mp3",
            initialdir=default_dir,
            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
            
    def show_file_info(self, filename):
        try:
            # Get file size
            file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
            
            # Get video info
            with VideoFileClip(filename) as video:
                duration = video.duration
                fps = video.fps
                resolution = f"{video.w}x{video.h}"
                has_audio = video.audio is not None
                
            info = f"File: {os.path.basename(filename)}\n"
            info += f"Size: {file_size:.1f} MB\n"
            info += f"Duration: {duration:.1f} seconds ({duration//60:.0f}m {duration%60:.0f}s)\n"
            info += f"Resolution: {resolution}\n"
            info += f"FPS: {fps:.1f}\n"
            info += f"Has Audio: {'Yes' if has_audio else 'No'}\n"
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)
            
        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, f"Error reading file info: {str(e)}")
            
    def start_conversion(self):
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input MP4 file")
            return
            
        if not self.output_file.get():
            messagebox.showerror("Error", "Please specify an output MP3 file")
            return
            
        if self.conversion_running:
            messagebox.showwarning("Warning", "Conversion is already running")
            return
            
        # Start conversion in a separate thread
        threading.Thread(target=self.convert_file, daemon=True).start()
        
    def convert_file(self):
        debug_info = []
        try:
            self.conversion_running = True
            self.convert_button.config(state='disabled')
            self.progress.start(10)
            self.status_label.config(text="Converting...", foreground="orange")
            
            # Perform conversion
            input_path = self.input_file.get()
            output_path = self.output_file.get()
            
            debug_info.append(f"Input path: {input_path}")
            debug_info.append(f"Output path: {output_path}")
            
            # Validate input file exists
            if not os.path.exists(input_path):
                raise Exception(f"Input file does not exist: {input_path}")
            debug_info.append("Input file exists: OK")
            
            # Validate output directory exists and is writable
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                raise Exception(f"Output directory does not exist: {output_dir}")
            debug_info.append(f"Output directory exists: {output_dir}")
            
            # Test write permissions
            try:
                test_file = os.path.join(output_dir, "test_write_permission.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                debug_info.append("Write permission test: OK")
            except Exception as perm_error:
                raise Exception(f"No write permission for directory: {output_dir}\nPermission error: {str(perm_error)}")
            
            # Load video with debug info
            debug_info.append("Loading video file...")
            try:
                video = VideoFileClip(input_path)
                debug_info.append(f"Video loaded successfully. Duration: {video.duration}")
                debug_info.append(f"Video FPS: {video.fps}")
                debug_info.append(f"Video resolution: {video.w}x{video.h}")
            except Exception as video_error:
                raise Exception(f"Failed to load video file: {str(video_error)}\nDebug info: {'; '.join(debug_info)}")
            
            # Check for audio track
            try:
                if video.audio is None:
                    video.close()
                    raise Exception(f"The selected video file has no audio track\nDebug info: {'; '.join(debug_info)}")
                debug_info.append("Audio track found: OK")
                
                # Extract audio with detailed error handling
                audio = video.audio
                if audio is None:
                    video.close()
                    raise Exception(f"Could not extract audio from video file\nDebug info: {'; '.join(debug_info)}")
                debug_info.append("Audio extracted: OK")
                
                # Attempt conversion with minimal parameters for exe compatibility
                debug_info.append("Starting audio conversion...")
                try:
                    # For executable compatibility, use a more direct approach
                    if getattr(sys, 'frozen', False):
                        # Running as executable - use simplified approach
                        debug_info.append("Executable environment detected - using simplified conversion")
                        # Don't store audio in a variable to avoid reference issues
                        video.audio.write_audiofile(output_path, logger=None)
                    else:
                        # Running as script - use standard approach
                        debug_info.append("Script environment detected - using standard conversion")
                        audio.write_audiofile(output_path)
                    debug_info.append("Audio conversion completed: OK")
                except Exception as conv_error:
                    # If the above fails, try alternative conversion method
                    debug_info.append("Primary conversion failed, trying alternative method...")
                    try:
                        # Alternative: Close and reload the video clip
                        video.close()
                        with VideoFileClip(input_path) as fresh_video:
                            if fresh_video.audio is not None:
                                fresh_video.audio.write_audiofile(output_path, logger=None)
                                debug_info.append("Alternative conversion succeeded: OK")
                            else:
                                raise Exception("No audio track in reloaded video")
                    except Exception as alt_error:
                        raise Exception(f"Both conversion methods failed:\nPrimary: {str(conv_error)}\nAlternative: {str(alt_error)}\nDebug info: {'; '.join(debug_info)}")
                finally:
                    # Ensure resources are cleaned up
                    try:
                        if 'audio' in locals() and audio is not None:
                            audio.close()
                        video.close()
                    except:
                        pass
                        
            except Exception as audio_error:
                try:
                    video.close()
                except:
                    pass
                raise audio_error
                
            # Conversion completed
            self.root.after(0, self.conversion_complete)
            
        except Exception as e:
            error_message = f"{str(e)}\n\nDetailed Debug Information:\n{chr(10).join(debug_info)}"
            self.root.after(0, lambda: self.conversion_error(error_message))
            
    def conversion_complete(self):
        self.conversion_running = False
        self.convert_button.config(state='normal')
        self.progress.stop()
        self.status_label.config(text="Conversion completed successfully!", foreground="green")
        
        # Show file size of output
        try:
            output_size = os.path.getsize(self.output_file.get()) / (1024 * 1024)
            current_info = self.info_text.get(1.0, tk.END)
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, current_info + f"\nOutput MP3 Size: {output_size:.1f} MB")
        except:
            pass
            
        messagebox.showinfo("Success", f"Conversion completed!\nFile saved as: {self.output_file.get()}")
        
    def conversion_error(self, error_message):
        self.conversion_running = False
        self.convert_button.config(state='normal')
        self.progress.stop()
        self.status_label.config(text="Conversion failed", foreground="red")
        
        # Add system information for debugging exe issues
        system_info = []
        system_info.append(f"Python executable: {sys.executable}")
        system_info.append(f"Running from: {'Executable' if getattr(sys, 'frozen', False) else 'Script'}")
        system_info.append(f"Current working directory: {os.getcwd()}")
        system_info.append(f"Temp directory: {os.environ.get('TEMP', 'Not found')}")
        
        # Check if FFmpeg is available
        try:
            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            system_info.append(f"FFmpeg path: {ffmpeg_path}")
            system_info.append(f"FFmpeg exists: {os.path.exists(ffmpeg_path)}")
        except Exception as ffmpeg_error:
            system_info.append(f"FFmpeg check failed: {str(ffmpeg_error)}")
        
        full_error = f"{error_message}\n\n--- System Information ---\n{chr(10).join(system_info)}"
        
        messagebox.showerror("Conversion Error", f"Failed to convert file:\n\n{full_error}")


def main():
    root = tk.Tk()
    app = MP4ToMP3Converter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
