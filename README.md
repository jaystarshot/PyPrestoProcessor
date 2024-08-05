# In Dev/Exp Mode

Goal is to process presto pages in a Python process and evaluate models.

## To Test Scaffold

1. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Set your Hugging Face token as an environment variable:

    ```sh
    export HUGGINGFACE_HUB_TOKEN=your_hugging_face_token
    ```

4. Run the gRPC server:

    ```sh
    python server.py
    ```

5. Run the REST API:

    ```sh
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

6. Send a sample page:

    ```sh
    curl -X POST http://localhost:8000/process -H "Content-Type: application/json" -d '{"sliceBytes": "aGVsbG8=", "positionCount": 1, "uncompressedSizeInBytes": 12345, "pageCodecMarkers": "d29ybGQ=", "checksum": 6789}'
    ```
