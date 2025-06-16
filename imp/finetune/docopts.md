## Synopsis

```text
Usage:
  finetune qagen <jsondocs>
```

qagen parses a collection of docs and produces a file `<jsondocs>.qa`  suitable for finetuning:

```text
<jsondocs> is a filename containing is a collection of docs in json format:

{
  "document": "text",
  "document1": "text1"
}

it creates a <jsondocs>.qa in format:

{"messages": [
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "What is the capital of France?"},
  {"role": "assistant", "content": "The capital of France is Paris."}
]}

suitable for pretraining using unsloth
```


