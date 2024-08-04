# Rapid Prototyping with Django, htmx, and Tailwind CSS

### Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/django-htmx-tailwind/).

## Want to use this project?

1. Fork/Clone

1. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv && source venv/bin/activate
    ```

1. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

1. Configure Tailwind CSS:

    ```sh
    tailwindcss
    ```

5. Watch for the style changes from the templates and generate CSS file:

    ```sh
    tailwindcss -i ./static/src/main.css -o ./static/src/output.css --watch
    ```

6. Apply the migrations and run the Django development server:

    ```sh
    python manage.py migrate
    python manage.py runserver
    ```

7. Test at [http://localhost:8000/](http://localhost:8000/)

8. For production, you can use the minified version of CSS file:

    ```sh
    tailwindcss -i ./static/src/main.css -o ./static/src/output.css --minify
    ```