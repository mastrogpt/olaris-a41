import os, sys

def main(args):
    print("finetune qagen", args)
    print(sys.argv)
    print(os.getenv("OLLAMA_HOST"), os.getenv("AUTH"))