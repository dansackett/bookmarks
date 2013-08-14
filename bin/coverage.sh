py.test --cov-config .coveragerc \
        --cov-report html \
        --cov tests \
        --cov mydash/middleware.py \
        --cov bookmarks \
        --cov account \
        --cov auth \
        --cov reminders \
        --cov todolists \
        --cov notes \
        --cov tags && \
python -c "import webbrowser, os; \
           webbrowser.open('file://' + os.getcwd() + \
                           '/htmlcov/index.html')"
