from flask import Flask, request, render_template, redirect, url_for
import os
import pdf_to_images
import ocr_extraction
import page_classification
import key_value_extraction
import table_extraction
import post_processing

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)
    if file:
        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(pdf_path)
        process_pdf(pdf_path)
        return redirect(url_for("results", filename=file.filename))
    return redirect(request.url)


def check_pages(data):
    result = {}
    for page_key, page_value in data.items():
        if isinstance(page_value, dict) and page_value:
            result[page_key] = list(page_value.keys())
        else:
            result[page_key] = []  # pass an empty list

    return result


def process_pdf(pdf_path):
    base_dir = os.path.splitext(pdf_path)[0]
    pdf_to_images.convert_to_images(pdf_path)
    ocr_path = os.path.join(base_dir, "ocr_results.json")
    ocr_extraction.extract_text_from_images(base_dir)
    classfication_result = page_classification.classify_images(base_dir)
    classification_keys = check_pages(classfication_result)
    key_value_results = key_value_extraction.extract_key_info_from_ocr_results(
        ocr_path, classification_keys
    )
    table_result = table_extraction.extract_tables_from_images(base_dir)
    post_processing.extract_combined_information(
        classfication_result, key_value_results, table_result, base_dir
    )


@app.route("/results/<filename>")
def results(filename):
    # Add code to display results
    return f"Processed {filename}"


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(debug=True)
