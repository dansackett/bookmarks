py.test --cov-config .coveragerc \
        --cov-report html \
        --cov tests \
        --cov bookshelf/middleware.py \
        --cov bookmarks \
        --cov account \
        --cov auth \
        --cov tags && \
python -c "import webbrowser, os; \
           webbrowser.open('file://' + os.getcwd() + \
                           '/htmlcov/index.html')"
