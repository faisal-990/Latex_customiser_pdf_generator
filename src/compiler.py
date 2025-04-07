import subprocess
import os
from pathlib import Path


def compile_pdf():
    try:
        # Define absolute paths
        project_root = Path(__file__).parent.absolute()
        output_dir = project_root / "output"
        tex_file = output_dir / "output.tex"

        # Ensure directory exists
        output_dir.mkdir(exist_ok=True)

        # Verify source file exists
        if not tex_file.exists():
            raise FileNotFoundError(f"LaTeX source file not found: {tex_file}")

        # Run pdflatex from the output directory
        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-output-directory={output_dir}",
                str(
                    tex_file.name
                ),  # Use just the filename when running from output dir
            ],
            cwd=str(output_dir),  # Run from output directory
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Verify PDF was created
        pdf_path = output_dir / "output.pdf"
        if pdf_path.exists():
            print(f"✅ PDF successfully generated at: {pdf_path}")
            return True
        else:
            print("❌ PDF generation failed")
            print(f"LaTeX output:\n{result.stdout}")
            if result.stderr:
                print(f"Errors:\n{result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Compilation timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
        return False
