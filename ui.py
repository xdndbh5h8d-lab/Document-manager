from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QInputDialog,
    QTextEdit,
)

from .document_io import load_pdf, load_word, save_pdf, save_word
from .storage import AppStorage


class DocumentManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document Manager")
        self.resize(980, 670)

        self.storage = AppStorage()
        self.current_workspace = self.storage.get_workspace_names()[0]
        self.current_document_index = None
        self.current_file_path = None
        self.current_file_type = None

        self._setup_ui()
        self._refresh_workspace_list()
        self._refresh_document_list()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        workspace_label = QLabel("Arbeitsbereiche")
        self.workspace_list = QListWidget()
        self.workspace_list.setFixedWidth(220)
        self.workspace_list.itemClicked.connect(self._on_workspace_selected)

        self.add_workspace_button = QPushButton("Arbeitsbereich hinzufügen")
        self.add_workspace_button.clicked.connect(self._create_new_workspace)

        document_label = QLabel("Dokumente")
        self.document_list = QListWidget()
        self.document_list.setFixedWidth(220)
        self.document_list.itemClicked.connect(self._on_document_selected)

        open_docx_button = QPushButton("Word öffnen")
        open_docx_button.clicked.connect(self.open_word_document)

        open_pdf_button = QPushButton("PDF öffnen")
        open_pdf_button.clicked.connect(self.open_pdf_document)

        new_docx_button = QPushButton("Neue Word-Datei")
        new_docx_button.clicked.connect(self.create_new_word_document)

        new_pdf_button = QPushButton("Neue PDF-Datei")
        new_pdf_button.clicked.connect(self.create_new_pdf_document)

        save_button = QPushButton("Speichern")
        save_button.clicked.connect(self.save_document)

        self.title_label = QLabel("Kein Dokument geladen")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_path_input = QLineEdit()
        self.file_path_input.setReadOnly(True)
        self.text_editor = QTextEdit()
        self.text_editor.setAcceptRichText(False)
        self.text_editor.setPlaceholderText("Hier kannst du Text eingeben...")

        button_layout = QHBoxLayout()
        button_layout.addWidget(open_docx_button)
        button_layout.addWidget(open_pdf_button)
        button_layout.addWidget(new_docx_button)
        button_layout.addWidget(new_pdf_button)
        button_layout.addWidget(save_button)

        left_layout = QVBoxLayout()
        left_layout.addWidget(workspace_label)
        left_layout.addWidget(self.workspace_list)
        left_layout.addWidget(self.add_workspace_button)
        left_layout.addSpacing(12)
        left_layout.addWidget(document_label)
        left_layout.addWidget(self.document_list)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.title_label)
        right_layout.addWidget(self.file_path_input)
        right_layout.addLayout(button_layout)
        right_layout.addWidget(self.text_editor)

        main_layout = QHBoxLayout(central)
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

    def _refresh_workspace_list(self) -> None:
        self.workspace_list.clear()
        for name in self.storage.get_workspace_names():
            self.workspace_list.addItem(name)

        selected_items = self.workspace_list.findItems(self.current_workspace, Qt.MatchFlag.MatchExactly)
        if selected_items:
            self.workspace_list.setCurrentItem(selected_items[0])

    def _refresh_document_list(self) -> None:
        self.document_list.clear()
        documents = self.storage.get_documents(self.current_workspace)
        for document in documents:
            self.document_list.addItem(document.get("name", "Unbenannt"))

    def _on_workspace_selected(self, item) -> None:
        self.current_workspace = item.text()
        self.current_document_index = None
        self.current_file_path = None
        self.current_file_type = None
        self.file_path_input.clear()
        self.title_label.setText(f"Arbeitsbereich: {self.current_workspace}")
        self.text_editor.clear()
        self._refresh_document_list()

    def _on_document_selected(self, item) -> None:
        documents = self.storage.get_documents(self.current_workspace)
        for index, document in enumerate(documents):
            if document.get("name") == item.text():
                self.current_document_index = index
                self.current_file_path = Path(document.get("path")) if document.get("path") else None
                self.current_file_type = document.get("type")
                self.title_label.setText(f"Dokument: {document.get('name')}")
                self.file_path_input.setText(str(self.current_file_path) if self.current_file_path else "")
                if self.current_file_path and self.current_file_path.exists():
                    self._load_current_file()
                else:
                    self.text_editor.clear()
                return

    def _create_new_workspace(self) -> None:
        name, ok = QInputDialog.getText(self, "Neuer Arbeitsbereich", "Name des Arbeitsbereichs:")
        if not ok or not name.strip():
            return
        name = name.strip()
        if not self.storage.add_workspace(name):
            QMessageBox.warning(self, "Fehler", f"Ein Arbeitsbereich mit dem Namen '{name}' existiert bereits.")
            return
        self.current_workspace = name
        self.current_document_index = None
        self.current_file_path = None
        self.current_file_type = None
        self.file_path_input.clear()
        self.title_label.setText(f"Arbeitsbereich: {name}")
        self.text_editor.clear()
        self._refresh_workspace_list()
        self._refresh_document_list()

    def open_word_document(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Word-Datei öffnen", "", "Word Dateien (*.docx)")
        if not path:
            return
        try:
            content = load_word(path)
            self.text_editor.setPlainText(content)
            self.current_file_path = Path(path)
            self.current_file_type = "docx"
            self.file_path_input.setText(path)
            self.title_label.setText(f"Word-Dokument: {Path(path).name}")
            self._remember_document(self.current_file_path, "docx")
        except Exception as exc:
            QMessageBox.critical(self, "Fehler", f"Word-Datei konnte nicht geladen werden:\n{exc}")

    def open_pdf_document(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "PDF-Datei öffnen", "", "PDF Dateien (*.pdf)")
        if not path:
            return
        try:
            content = load_pdf(path)
            self.text_editor.setPlainText(content)
            self.current_file_path = Path(path)
            self.current_file_type = "pdf"
            self.file_path_input.setText(path)
            self.title_label.setText(f"PDF-Dokument: {Path(path).name}")
            self._remember_document(self.current_file_path, "pdf")
        except Exception as exc:
            QMessageBox.critical(self, "Fehler", f"PDF-Datei konnte nicht geladen werden:\n{exc}")

    def create_new_word_document(self) -> None:
        self.current_file_path = None
        self.current_file_type = "docx"
        self.current_document_index = None
        self.title_label.setText("Neue Word-Datei")
        self.file_path_input.clear()
        self.text_editor.setPlainText("Neue Word-Datei\n")

    def create_new_pdf_document(self) -> None:
        self.current_file_path = None
        self.current_file_type = "pdf"
        self.current_document_index = None
        self.title_label.setText("Neue PDF-Datei")
        self.file_path_input.clear()
        self.text_editor.setPlainText("Neue PDF-Datei\n")

    def save_document(self) -> None:
        content = self.text_editor.toPlainText()
        if not content.strip():
            QMessageBox.warning(self, "Warnung", "Der Textbereich ist leer. Bitte füge Inhalt hinzu.")
            return

        if self.current_file_type == "docx":
            self._save_word(content)
        elif self.current_file_type == "pdf":
            self._save_pdf(content)
        else:
            choice = QMessageBox.question(
                self,
                "Dateityp wählen",
                "Möchtest du das Dokument als Word oder PDF speichern?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if choice == QMessageBox.StandardButton.Yes:
                self.current_file_type = "docx"
                self._save_word(content)
            else:
                self.current_file_type = "pdf"
                self._save_pdf(content)

    def _save_word(self, content: str) -> None:
        path = self.current_file_path
        if not path or path.suffix.lower() != ".docx":
            path, _ = QFileDialog.getSaveFileName(self, "Word-Datei speichern", "", "Word Dateien (*.docx)")
            if not path:
                return
            path = Path(path if path.endswith(".docx") else f"{path}.docx")

        try:
            save_word(content, str(path))
            self.current_file_path = path
            self.file_path_input.setText(str(path))
            self.title_label.setText(f"Word-Dokument: {path.name}")
            self._remember_document(path, "docx")
            QMessageBox.information(self, "Erfolg", f"Word-Datei gespeichert:\n{path}")
        except Exception as exc:
            QMessageBox.critical(self, "Fehler", f"Word-Datei konnte nicht gespeichert werden:\n{exc}")

    def _save_pdf(self, content: str) -> None:
        path = self.current_file_path
        if not path or path.suffix.lower() != ".pdf":
            path, _ = QFileDialog.getSaveFileName(self, "PDF-Datei speichern", "", "PDF Dateien (*.pdf)")
            if not path:
                return
            path = Path(path if path.endswith(".pdf") else f"{path}.pdf")

        try:
            save_pdf(content, str(path))
            self.current_file_path = path
            self.file_path_input.setText(str(path))
            self.title_label.setText(f"PDF-Dokument: {path.name}")
            self._remember_document(path, "pdf")
            QMessageBox.information(self, "Erfolg", f"PDF-Datei gespeichert:\n{path}")
        except Exception as exc:
            QMessageBox.critical(self, "Fehler", f"PDF-Datei konnte nicht gespeichert werden:\n{exc}")

    def _remember_document(self, path: Path, document_type: str) -> None:
        document_name = path.name
        self.storage.add_document(
            self.current_workspace,
            document_name,
            str(path),
            document_type,
        )
        self.storage.add_recent_file(str(path))
        self._refresh_document_list()
        self._select_document_in_list(document_name)

    def _select_document_in_list(self, document_name: str) -> None:
        items = self.document_list.findItems(document_name, Qt.MatchFlag.MatchExactly)
        if items:
            self.document_list.setCurrentItem(items[0])

    def _load_current_file(self) -> None:
        if not self.current_file_path or not self.current_file_path.exists():
            return
        try:
            if self.current_file_type == "docx":
                self.text_editor.setPlainText(load_word(str(self.current_file_path)))
            elif self.current_file_type == "pdf":
                self.text_editor.setPlainText(load_pdf(str(self.current_file_path)))
        except Exception as exc:
            QMessageBox.warning(self, "Warnung", f"Datei konnte nicht geladen werden:\n{exc}")
