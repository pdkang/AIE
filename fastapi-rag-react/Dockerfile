FROM python:3.9

WORKDIR /code

# Create backend directory first
RUN mkdir -p /code/backend

# Copy all required files
COPY ./requirements.txt /code/requirements.txt
COPY ./backend/__init__.py /code/backend/
COPY ./backend/main.py /code/backend/
COPY ./backend/text_utils.py /code/backend/
COPY ./backend/openai_utils.py /code/backend/
COPY ./backend/vector_store.py /code/backend/
COPY ./frontend/dist /code/frontend/dist

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Set Python path to include the backend directory
ENV PYTHONPATH=/code

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]