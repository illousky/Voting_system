AUTHOR:

    - Ignacio Gonzalez Porras


EXECUTION GUIDE:

    - System done for running as daemon using gunicorn. Install gunicorn and copy and paste the
    gunicorn_config.txt file in a new file using: sudo nano /etc/systemd/system/gunicorn.service
    - Run gunicorn using:
        1) sudo systemctl daemon-reload
        2) sudo systemctl enable gunicorn
        3) sudo systemctl start gunicorn
        4) sudo systemctl status gunicorn
    and then make sure gunicorn y running correctly.
    - Once gunicorn is running, you can access to the service by searching the following URL: 
    http://localhost:8000/votoApp/censo/. You can change the port to any you put in the gunicorn
    configuration file.

    - For running both rpc-server and ws-server, you must run their clients too. If not, you won't
    have access to the system.
    -To run the clients, execute "python3 manage.py runserver 0.0.0.0:8001" on the directory you want
    to run. Of course, you can select the port you want to use. 
    - Then access with the same URL mentioned before.