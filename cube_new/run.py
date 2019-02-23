#! /usr/bin/python3

from cube import check_dependencies, create_app

check_dependencies()
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
