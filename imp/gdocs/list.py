import common

def list_folder(FOLDER):

    drive_sv = common.drive_sv()
    if drive_sv is None:
        print("Cannot Connet to Google Drive - check you have a .google.json")
    
    FID = common.get_id(FOLDER, "folder")
    if FID is None:
        print("Cannot get ID from URL")
        return
    
    result = []
    page_token = None
    while True:
        response = drive_sv.files().list(
            q=f"'{FID}' in parents and trashed = false",
            pageToken=page_token
        ).execute()
        result.extend(response.get('files', []))
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return {'files': result}
    

def main(argv):
    """
    List Folder
    """
    [FOLDER] = argv
    
    result = list_folder(FOLDER)
    for file in result.get("files", []):
        print(f"https://docs.google.com/document/d/{file.get('id', '')}\t{file.get('name', '')}")
    
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])