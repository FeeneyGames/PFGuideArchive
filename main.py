from gdrive import DriveDownloader


CRED_PATH = "pathfinderguidesguide-ace77dd25e21.json"
d_downloader = DriveDownloader(CRED_PATH)
test_file_id = "1hChbcEsEfQsR7NkwKlzO-GLYtrOtxlkGHpRQgKKZ5gc"
print(d_downloader.get_doc_type(test_file_id))
