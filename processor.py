import presto_pb2
import torch
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the Hugging Face token from the environment variable
token = os.getenv("HUGGINGFACE_HUB_TOKEN")
if not token:
    raise ValueError("HUGGINGFACE_HUB_TOKEN environment variable not set")

# Load the model and tokenizer
model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct")
model.eval()  # Set the model to evaluation mode

def process_presto_page(page: presto_pb2.GrpcSerializedPage) -> presto_pb2.GrpcSerializedPage:
    # Decode the input bytes to string
    input_text = page.sliceBytes.decode('utf-8')

    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt")

    # Generate the response using the model
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=50)

    # Decode the generated tokens to string
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Encode the output text back to bytes
    output_bytes = output_text.encode('utf-8')

    # Create a new GrpcSerializedPage message with the processed output
    return presto_pb2.GrpcSerializedPage(
        sliceBytes=output_bytes,
        positionCount=page.positionCount,
        uncompressedSizeInBytes=page.uncompressedSizeInBytes,
        pageCodecMarkers=page.pageCodecMarkers,
        checksum=page.checksum
    )
