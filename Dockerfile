# Back-end Build Steps
FROM python:3.11
RUN python3 -m pip install --upgrade pip
COPY ./backend/requirements.txt /workspace/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /workspace/backend/requirements.txt
COPY --from=build /workspace/static /workspace/static
COPY ./backend /workspace/backend
WORKDIR /workspace
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
ENV TZ="America/New_York"
EXPOSE 8080