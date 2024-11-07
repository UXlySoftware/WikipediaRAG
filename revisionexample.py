import mwxml

dump = mwxml.Dump.from_file(open("Wiki-revision-example-Fayum-Portraits.xml"))

for page in dump:
    print(page.id, page.title)
    for revision in page:
        print(revision.id, revision.timestamp, revision.user)
        print(revision.text)
        print()