import os
import json
from dataclasses import dataclass
from typing import Optional

from app.services.detect.main import process_image

# Caminho absoluto para o script de detecção
DETECTION_SCRIPT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "detect",
    "main.py"
)


@dataclass
class DetectionResult:
    output_folder: str
    gags_score: int
    gags_severity: str
    region_counts: dict
    image_path: str
    error: Optional[str]

    @property
    def result_json_path(self) -> str:
        return os.path.join(self.output_folder, "result.json")

    @property
    def result_image_path(self) -> str:
        return os.path.join(self.output_folder, "detected_image.jpg")


class DetectionService:

    def run(
        self,
        image_path: str,
        consulta_id: str,
        conf: float = 0.25
    ) -> DetectionResult:
        
        self._validate_inputs(image_path)

        output = self._run_subprocess(image_path, consulta_id, conf)
        output_folder = self._parse_subprocess_output(output)
        result_data = self._read_result_json(output_folder)

        return DetectionResult(
            output_folder=output_folder,
            gags_score=result_data.get("gags_score", 0),
            gags_severity=result_data.get("gags_severity", "Error"),
            region_counts=result_data.get("region_counts", {}),
            image_path=result_data.get("image_path", ""),
            error=result_data.get("error")
        )

    # ------------------------------------------------------------------
    # Métodos privados
    # ------------------------------------------------------------------

    def _validate_inputs(self, image_path: str) -> None:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

        if not os.path.exists(DETECTION_SCRIPT_PATH):
            raise FileNotFoundError(
                f"Script de detecção não encontrado: {DETECTION_SCRIPT_PATH}"
            )

    def _run_subprocess(
        self,
        image_path: str,
        consulta_id: str,
        conf: float
    ) -> str:
        try:
            output_folder = process_image(consulta_id=consulta_id, image_path=image_path, conf=conf)
        except Exception as e:
            raise RuntimeError(
                f"Falha ao executar o processo de detecção: {type(e).__name__}: {e}"
            )

        if not output_folder:
            raise RuntimeError("O processo de detecção não retornou pasta de saída.")

        return output_folder

    def _parse_subprocess_output(self, raw_output: str) -> str:
        """Retorna a pasta de saída diretamente quando o processo é chamado internamente."""
        if not raw_output:
            raise RuntimeError("O processo de detecção não retornou nenhuma saída.")

        return raw_output
    def _read_result_json(self, output_folder: str) -> dict:
        """Lê o result.json gerado pelo script."""
        result_path = os.path.join(output_folder, "result.json")

        if not os.path.exists(result_path):
            raise RuntimeError(
                f"result.json não encontrado em: {output_folder}"
            )

        with open(result_path, "r", encoding="utf-8") as f:
            return json.load(f)