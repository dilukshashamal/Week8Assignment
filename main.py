import pdf_to_images
import page_classification
import os
import argparse
import key_value_extraction
import ocr_extraction
import table_extraction
import post_processing


def check_pages(data):
    result = {}
    for page_key, page_value in data.items():
        if isinstance(page_value, dict) and page_value:
            result[page_key] = list(page_value.keys())
        else:
            result[page_key] = []  # pass an empty list

    return result


if __name__ == "__main__":
    # set of arguments
    parser = argparse.ArgumentParser(description="Arguments needed to extract pdf")
    parser.add_argument("pdf_path", type=str, help="Path to the pdf file to execute")

    args = parser.parse_args()
    pdf_path = args.pdf_path
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
