import os
from Scripts.EncryptDecryptFunctions import sign_hash, hash_document
from Scripts.EncryptDecryptFunctions import get_file_metadata
import datetime


def create_xades_xml(file_path, signature, metadata, signing_window):
    signing_window.appendText("metadane pliku")
    signing_window.appendText("rozmiar: " + metadata["size"])
    signing_window.appendText("Metadane ostatnia modyfikacja: " + metadata["last_modified"])
    signing_window.appendText("Metadane rozszerzenie: " + metadata["extension"])
    signing_window.appendText("Metadane autor pliku: " + metadata["author"])

    directory = os.path.dirname(file_path)
    xml_file_path = os.path.join(directory, "xades_signature.xml")
    with open(xml_file_path, "w", encoding="UTF-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<xades:Signature xmlns="http://uri.etsi.org/01903/v1.3.2#" '
                'xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" '
                'Id="Signature">\n')

        f.write('  <xades:SignedInfo>\n')
        f.write('    <ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256" />\n')
        f.write('  </xades:SignedInfo>\n')

        f.write('  <ds:SignatureValue>' + signature + '</ds:SignatureValue>\n')

        f.write('  <xades:Object>\n')
        f.write('    <xades:QualifyingProperties>\n')
        f.write('      <xades:SignedProperties>\n')
        f.write('        <xades:SignedSignatureProperties>\n')
        f.write('          <xades:SigningTime>' + datetime.datetime.now().isoformat() + '</xades:SigningTime>\n')
        f.write('        </xades:SignedSignatureProperties>\n')
        f.write('      </xades:SignedProperties>\n')
        f.write('    </xades:QualifyingProperties>\n')
        f.write('  </xades:Object>\n')

        f.write('  <xades:AdditionalInfo>\n')
        f.write('    <xades:Extension>' + metadata["extension"] + '</xades:Extension>\n')
        f.write('    <xades:LastModified>' + metadata["last_modified"] + '</xades:LastModified>\n')
        f.write('    <xades:Author>' + metadata["author"] + '</xades:Author>\n')
        f.write('    <xades:Size>' + metadata["size"] + '</xades:Author>\n')
        f.write('  </xades:AdditionalInfo>\n')

        f.write('</xades:Signature>\n')
        signing_window.appendText("Podpisano dokument, plik .xml znajduje się w " + str(xml_file_path))


def sing_document(file_path, signing_window):
    document_hash = hash_document(file_path)
    signature = sign_hash(document_hash).hex()
    signing_window.appendText("hash pliku:" + str(document_hash))
    metadata = get_file_metadata(file_path)
    create_xades_xml(file_path, signature, metadata, signing_window)
