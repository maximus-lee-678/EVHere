EVHere Prototype
================

| Originally developed under the name **team_15_flask_react**, with the goal of
| **Webpage development and data processing for electric vehicle charging management and machine learning analysis**.
|
* Includes an interactive webpage which supports the display of and interaction with Electric Vehicle chargers in Singapore.
* Machine Learning is performed on Historical EV data to predict upcoming prices.
* Photovoltaic voltage is able to be read from Solar Panels and uploaded to the Website Backend Database.

.. image:: https://github.com/maximus-lee-678/team_15_flask_react/blob/main/other/webpage_screenshot.jpg
  :alt: EVHere Webpage

👥 Team Members
----------------

.. list-table::
   :header-rows: 1

   * - Name
     - Role
   * - `Sing Yu <https://github.com/Uygnis>`_
     - Team Lead + Machine Learning
   * - `Maximus Lee <https://github.com/maximus-lee-678>`_
     - Backend Lead + Frontend
   * - `Yong Zhi Wei <https://github.com/zoee-Y>`_
     - Frontend Lead
   * - `Yi Kiat <https://github.com/yi-kiat>`_
     - Raspberry PI
   * - Samantha Tan
     - Raspberry PI

🛠 Setup (Webpage)
------------------

1. Download and install `Node JS <https://nodejs.org/en/>`_.

2. To initialise backend python packages, run:

.. code-block:: console

  pip install -r requirements.txt

3. To initialise backend database with random values, run:

.. code-block:: console

  generate_db_files.bat

4. To initialise frontend node packages, run:

.. code-block:: console

  cd react && update.bat

5. Once steps 1-4 are completed, run the server with:

.. code-block:: console

  start.bat

| On the first run, the Flask backend may take a while to initialise database values.
| This may cause frontend errors since the backend is unresponsive.
| Simply wait for the backend to load and the webpage will function normally again.


📗 Documentation
----------------

.. code-block:: console

  cd docs\html && index.html

🗜 Technologies
---------------

* Website Backend

  * `Python Flask <https://flask.palletsprojects.com/en/3.0.x/>`_
  * `SQLite <https://docs.python.org/3/library/sqlite3.html>`_

* Website Frontend

  * `Node.js <https://nodejs.org/en>`_
  * `React <https://react.dev/>`_
  * `tailwind.css <https://tailwindcss.com/>`_

* Website Documentation

  * `Python Sphinx <https://www.sphinx-doc.org/en/master/>`_
  * `Sphinx Docs <https://sublime-and-sphinx-guide.readthedocs.io/en/latest/index.html>`_

* Machine Learning

  * `PyTorch <https://pytorch.org/>`_
  * `Darts <https://unit8co.github.io/darts/>`_
  * `Weights and Biases <https://docs.wandb.ai/>`_

* Sensors

  * `Raspberry Pi <https://www.raspberrypi.org/>`_
  * `Python Locust <https://locust.io/>`_
