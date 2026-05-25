import json
from pathlib import Path
from typing import Any

DEFAULT_DATA = {
    "workspaces": [
        {
            "name": "Allgemein",
            "documents": [],
        }
    ],
    "recent_files": [],
}


class AppStorage:
    def __init__(self, filename: str = "app_data.json"):
        self.path = Path(filename)
        self.data = self._load_default_data()
        self.load()

    def _load_default_data(self) -> dict[str, Any]:
        return json.loads(json.dumps(DEFAULT_DATA))

    def load(self) -> None:
        if self.path.exists():
            try:
                raw = self.path.read_text(encoding="utf-8")
                self.data = json.loads(raw)
            except Exception:
                self.data = self._load_default_data()
        else:
            self.data = self._load_default_data()
            self.save()

    def save(self) -> None:
        self.path.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def get_workspace_names(self) -> list[str]:
        return [workspace["name"] for workspace in self.data["workspaces"]]

    def get_workspace(self, workspace_name: str) -> dict[str, Any] | None:
        for workspace in self.data["workspaces"]:
            if workspace["name"] == workspace_name:
                return workspace
        return None

    def add_workspace(self, workspace_name: str) -> bool:
        if self.get_workspace(workspace_name) is not None:
            return False
        self.data["workspaces"].append({"name": workspace_name, "documents": []})
        self.save()
        return True

    def add_document(
        self,
        workspace_name: str,
        document_name: str,
        document_path: str,
        document_type: str,
    ) -> None:
        workspace = self.get_workspace(workspace_name)
        if workspace is None:
            return

        documents = workspace["documents"]
        for document in documents:
            if document.get("path") == document_path:
                document.update({"name": document_name, "type": document_type})
                self.save()
                return

        documents.append(
            {
                "name": document_name,
                "path": document_path,
                "type": document_type,
            }
        )
        self.save()

    def update_document(
        self,
        workspace_name: str,
        document_index: int,
        document_name: str,
        document_path: str,
        document_type: str,
    ) -> None:
        workspace = self.get_workspace(workspace_name)
        if workspace is None:
            return

        documents = workspace["documents"]
        if 0 <= document_index < len(documents):
            documents[document_index] = {
                "name": document_name,
                "path": document_path,
                "type": document_type,
            }
            self.save()

    def get_documents(self, workspace_name: str) -> list[dict[str, Any]]:
        workspace = self.get_workspace(workspace_name)
        if workspace is None:
            return []
        return workspace["documents"]

    def add_recent_file(self, document_path: str) -> None:
        recent = [path for path in self.data["recent_files"] if path != document_path]
        recent.insert(0, document_path)
        self.data["recent_files"] = recent[:10]
        self.save()
