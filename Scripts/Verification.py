from Scripts.EncryptDecryptFunctions import verify_signature, get_file_metadata, hash_document
import re


def extract_xml_value(xml_content, tag):
    pattern = rf"{re.escape(tag)}(.*?)</"
    match = re.search(pattern, xml_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        print(f"Nie znaleziono wartości {tag} w pliku XML.")
        return None


def verify(xml_file_path, file_path, window):
    with open(xml_file_path, "r", encoding="UTF-8") as f:
        xml_content = f.read()
    signature = extract_xml_value(xml_content, "<ds:SignatureValue>")
    extension = extract_xml_value(xml_content, "<xades:Extension>")
    author = extract_xml_value(xml_content, "<xades:Author>")
    size = extract_xml_value(xml_content, "<xades:Size>")
    last_modified = extract_xml_value(xml_content, "<xades:LastModified>")
    metadata = get_file_metadata(file_path)
    window.appendText("Metadane zapisane w podpisie i metadane pliku:")
    window.appendText("Rozszerzenie: " + str(extension) + " " + metadata["extension"])
    window.appendText("Rozmiar: " + str(size) + " " + metadata["size"])
    window.appendText("Autor: " + str(author) + " " + metadata["author"])
    window.appendText("Ostatnia modyfikacja: " + str(last_modified) + " " + metadata["last_modified"])

    document_hash = hash_document(file_path)
    verify_signature(signature.encode(), document_hash, window)




