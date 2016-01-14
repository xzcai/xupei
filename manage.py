from flask_script import Manager, Server

import src

manager = Manager(src.app)
manager.add_command("runserver", Server('0.0.0.0', port=8878))

# Application = app

if __name__ == '__main__':
    # manager.run()
    src.app.run(debug=True, host='0.0.0.0', port=8878)