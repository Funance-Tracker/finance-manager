import tkinter as tk
from tkinter import ttk
from GUI.report import TransactionReportApp
from GUI.files_reader import FilesReaderPage
from voice import VoiceCommandApp

class SideButtons(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Ensure the frame expands vertically and is sticky to the north and south
        self.grid(row=1, column=0, sticky="ns")

        # Buttons
        ttk.Button(self, text="Report", command=self.open_report).pack(pady=5, padx=10, anchor="n")
        ttk.Button(self, text="File Reader", command=self.open_file_reader).pack(pady=5, padx=10, anchor="n")
        ttk.Button(self, text="Voice", command=self.voice_command).pack(pady=5, padx=10, anchor="n")

    def open_report(self):
        TransactionReportApp(self.controller.user_info['id'])

    def voice_command(self):
        VoiceCommandApp(self.controller.user_info['id'])

    def open_file_reader(self):
        FilesReaderPage(self.controller.user_info['id'])
