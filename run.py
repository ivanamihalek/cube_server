#! /usr/bin/python3

from cube import check_dependencies, create_app

app = create_app()
check_dependencies()


if __name__ == '__main__':
    app.run(debug=True)
