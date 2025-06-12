import sys
#print(sys.argv)
if sys.argv[1] == "list":
    import gdocs.list
    gdocs.list.main(sys.argv[2:])
elif sys.argv[1] == "parse":
    import gdocs.parse
    gdocs.parse.main(sys.argv[2:])
elif sys.argv[1] == "import":
    import gdocs.importer
    gdocs.importer.main(sys.argv[2:])    