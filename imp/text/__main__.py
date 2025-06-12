import sys
import text.csvimp
print(sys.argv)
if sys.argv[1] == "csvimp":
    import text.csvimp
    text.csvimp.main(sys.argv[2:])    