import arrow_service_pb2
import pyarrow as pa
import pandas
import transformers
import torch
import os

# Check if the environment variable is set
if "HUGGING_FACE_HUB_TOKEN" not in os.environ:
    raise EnvironmentError("Environment variable 'HUGGING_FACE_HUB_TOKEN' is not set. Please set it to proceed.")

os.environ["HUGGING_FACE_HUB_TOKEN"] = "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"


# Set model ID and local directory
# model_id = "meta-llama/Meta-Llama-3.1-8B"
# local_model_dir = "./local_meta_llama_3.1_8B"

model_id = "distilbert/distilgpt2"
local_model_dir = "./distilbert/distilgpt2"

device = f'cuda:{torch.cuda.current_device()}' if torch.cuda.is_available() else 'cpu'


# Check if the model is already saved locally
if os.path.exists(local_model_dir):
    print(f"Loading model {model_id} from local checkpoint...")
    text_generator = transformers.pipeline(
        "text-generation",
        model=local_model_dir,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto"
    )
else:
    print(f"Downloading model {model_id} from Hugging Face and saving locally...")
    text_generator = transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto"
    )
    # Save the model and tokenizer locally for future use
    text_generator.model.save_pretrained(local_model_dir)
    text_generator.tokenizer.save_pretrained(local_model_dir)

print(f"Model loaded on {device}")

def process_presto_page(page: arrow_service_pb2.ArrowArrayRequest):
    try:
        print("Received Input")
        print(page.data)
        # Wrap the serialized data in a BufferReader
        buffer = pa.BufferReader(page.data)

        # Use RecordBatchStreamReader to read the schema and batch
        reader = pa.ipc.RecordBatchStreamReader(buffer)
        table = reader.read_all()

        assert table.schema[0].type == pa.string(), "First column must be of type string"
        assert table.schema[1].type == pa.string(), "Second column must be of type prompt"
         # Convert the Arrow Table to a Pandas DataFrame
        df = table.to_pandas()
        print(df)

        print("Shape = {}".format(df.shape))
          # Concatenate c0 and c1, handling None values in c1
        df['combined_prompt'] = df['c0'] + " " + df['c1'].fillna('')

        generated_texts = text_generator(df['combined_prompt'].tolist(), max_length=40)
         # Extract generated texts from the results
        print("Generated Texts Output:")
        # print(generated_texts)
        df['c1'] = [text[0]['generated_text'] for text in generated_texts]
        # print(df['generated_text'])

        # Convert the DataFrame with generated text back to an Arrow Table
        # output_table = pa.Table.from_pandas(df[['generated_text']])
        print("Generated Pandas Output:")
        print(df[['c0', 'c1']])
        # Create the Arrow Table with 'c0' and 'c1' columns
        output_table = pa.Table.from_pandas(df[['c0', 'c1']])

        print("Generated Arrow Output:")
        # Serialize the Arrow Table to bytes
        sink = pa.BufferOutputStream()
        with pa.ipc.new_stream(sink, output_table.schema) as writer:
            writer.write_table(output_table)

        # This will still contain some metadata but as minimal as possible
        arrow_data = sink.getvalue().to_pybytes()
        print(arrow_data)
        print("Size of serialized Arrow data:", len(arrow_data))
        # Return the serialized bytes in the ArrowArrayResponse
        return arrow_service_pb2.ArrowArrayResponse(data=arrow_data)


    except Exception as e:
        print(f"Failed to deserialize Arrow data: {e}")
    print("Came here")
    # Return the original data for completeness
    return arrow_service_pb2.ArrowArrayResponse(data=page.data)
