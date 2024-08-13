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

