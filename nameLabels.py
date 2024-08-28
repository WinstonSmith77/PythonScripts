from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from pathlib import Path


def create_pdf_labels(labels, filename):
    c = canvas.Canvas(filename, pagesize=A4)

    # Set label dimensions
    label_width = 30 * mm
    label_height = 12 * mm

    # Set label margins
    left_margin = 2 * mm
    bottom_margin = 2 * mm

    # Iterate over labels and draw them on the canvas
    for i, label_text in enumerate(labels):
        # Calculate label position
        x = left_margin + (i % 3) * label_width
        y = bottom_margin + (i // 3) * label_height

        # Draw label text
        c.drawString(x, y, label_text)

    # Save the canvas as a PDF file
    c.save()

# Example usage
labels = ["Label 1", "Label 2", "Label 3", "Label 4", "Label 5", "Label 6"]
filename = Path(Path(__file__).parent, 'lables.pdf')
create_pdf_labels(labels, str(filename))