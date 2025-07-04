import os, sys
from dotenv import load_dotenv
load_dotenv(dotenv_path= os.path.join(os.getenv("OPS_PWD"), ".env"))
load_dotenv(dotenv_path= os.path.join(os.getenv("OPS_PWD"), "packages", ".env"))

print("finetune", sys.argv)
if sys.argv[1] == "qagen":
    import finetune.qagen
    finetune.qagen.main(sys.argv[2:])
