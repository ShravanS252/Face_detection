import dropbox
dropbox_access_token= "sl.BWrTTpSF2eMDndo_Im8DFEmlQVzwBO-F6sFKgrCHJ6Kt1lvVALRqj-FZt8lrrxJf78aHKUf_XLivI_LfKaDo_gR86-GwnCFrmkn6cnk00fmK2gQ0VSslE4NQXhExFTqLkR2139CXLvU"    #Enter your own access token
dropbox_path= "/detection/img2.jpg"
computer_path="img2.jpg"

client = dropbox.Dropbox(dropbox_access_token)
print("[SUCCESS] dropbox account linked")
client.files_upload(open(computer_path, "rb").read(), dropbox_path)
print("[UPLOADED] {}".format(computer_path))