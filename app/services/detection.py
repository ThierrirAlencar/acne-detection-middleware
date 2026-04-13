import os
import json
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional

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
        """
        Executa o script de detecção de acne como subprocesso.

        Args:
            image_path:  Caminho absoluto para a imagem de entrada.
            consulta_id: ID da consulta/inquiry (usado para organizar as pastas de saída).
            conf:        Limiar de confiança do YOLO (padrão 0.25).

        Returns:
            DetectionResult com todos os dados do processamento.

        Raises:
            FileNotFoundError: Se a imagem ou o script não existirem.
            RuntimeError:      Se o subprocesso falhar ou a saída for inválida.
        """
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
        """Executa o script e retorna o stdout."""
        command = [
            sys.executable,          # mesmo interpretador Python do ambiente
            DETECTION_SCRIPT_PATH,
            "--image", image_path,
            "--consulta_id", str(consulta_id),
            "--conf", str(conf),
        ]

        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120  # 2 minutos — YOLO pode demorar na primeira inferência
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("O processo de detecção excedeu o tempo limite (120s).")
        except Exception as e:
            raise RuntimeError(f"Falha ao iniciar o subprocesso: {e}")

        if process.returncode != 0:
            raise RuntimeError(
                f"O script de detecção retornou erro (código {process.returncode}).\n"
                f"stderr: {process.stderr.strip()}"
            )

        return process.stdout.strip()

    def _parse_subprocess_output(self, raw_output: str) -> str:
        """Extrai o output_folder do JSON impresso pelo script."""
        if not raw_output:
            raise RuntimeError("O script não retornou nenhuma saída.")

        # O script pode emitir logs antes do JSON; pega só a última linha
        last_line = raw_output.splitlines()[-1]

        try:
            data = json.loads(last_line)
        except json.JSONDecodeError:
            raise RuntimeError(
                f"Saída do script não é um JSON válido: {last_line!r}"
            )

        output_folder = data.get("output_folder")
        if not output_folder:
            raise RuntimeError("JSON de saída não contém 'output_folder'.")

        return output_folder

    def _read_result_json(self, output_folder: str) -> dict:
        """Lê o result.json gerado pelo script."""
        result_path = os.path.join(output_folder, "result.json")

        if not os.path.exists(result_path):
            raise RuntimeError(
                f"result.json não encontrado em: {output_folder}"
            )

        with open(result_path, "r", encoding="utf-8") as f:
            return json.load(f)