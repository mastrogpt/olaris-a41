import os, common
from tika import parser

def download_doc(drive_sv, DID):
    """
    Download the document from the drive service and store in a temp file
    Return the temp file path
    """
    try:
        # Get the file metadata
        file = drive_sv.files().get(fileId=DID).execute()
        if not file:
            return None
            
        # Download the actual file content
        #info = drive_sv.files().get(fileId=DID, fields="id, name, mimeType").execute()
        #mime = info.get("mimeType", "")
        
        #detect a file is in google doc format and download the content
        name = file.get("name")
        mime = file.get("mimeType")
        print("===",name,mime)
        if mime== "application/vnd.google-apps.document":
            #export the content
            content = drive_sv.files().export_media(fileId=DID, mimeType="text/plain").execute()
        else:
            #download the content
            content = drive_sv.files().get_media(fileId=DID).execute()
            
        # remove empty lines

        # Write to temp file
        import tempfile
        temp = tempfile.NamedTemporaryFile(delete=False, mode='wb')
        temp.write(content)
        temp.close()
        filename = temp.name
        return filename, name
        
    except Exception as e:
        print(f"Error downloading document: {e}")
        return None


def extract_text_and_remove(filename):
    parsed = parser.from_file(filename)
    os.unlink(filename)
    return parsed.get("content")


def parse_doc(DID):
    drive_sv = common.drive_sv()
    filename, name = download_doc(drive_sv, DID)
    text = extract_text_and_remove(filename)
    text = "\n".join([line for line in text.split("\n") if line.strip() != ""])
    return name, text

def main(argv):
    """
    Parse Document
    """
    [DOC, FILE] = argv
    print(DOC)

    drive_sv = common.drive_sv()
    if drive_sv is None:
        print("Cannot Connect to Google Drive - check you have a .google.json")
    
    DID = common.get_id(DOC, "doc")
    print(DID)
    _, text = parse_doc(DID)

    if FILE == "":
        print(text) 
    else:
        os.chdir(os.getenv("OPS_PWD"))
        with open(FILE, "w") as f:
            f.write(text)
        print(f"Saved to {FILE}.")
    
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])