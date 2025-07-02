import sys
import text.csvimp
if sys.argv[1] == "csvimp":
    import text.csvimp
    text.csvimp.main(sys.argv[2:])
elif sys.argv[1] == "dirimp":
    import text.dirimp
    text.dirimp.main(sys.argv[2:])        
else:
    print(sys.argv)
    print("Unknown command")