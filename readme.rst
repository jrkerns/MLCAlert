MLCAlert
--------

MLCAlert is a script based on the paper by `Wu et al: Utilizing historical MLC performance data from trajectory
logs and service reports to establish a proactive maintenance model for minimizing treatment disruptions
<https://aapm.onlinelibrary.wiley.com/doi/10.1002/mp.13363>`_. The idea is to analyze your trajectory logs to look for
deviations in the expected/actual values of the leaves. If there are too many deviations an email is triggered.
The script can be set up to run automatically with a tool like cron or Windows Task Scheduler.

While this initial version is faithful to the manuscript, there are drawbacks to it. Namely, the triggers are not normalized
to the distance traveled by the leaf. I.e. if your clinic is busy in general or your outer leaves move far less than your
inner leaves (which is almost always the case) then this algorithm will not be as sensitive as it could be. Future versions
will include leaf travel normalization.

.. note::

    Currently, the script is only for Trajectory logs from a TrueBeam. Dynalogs will be supported in a future version.

Setup
^^^^^

There are four parts to getting the script working. If you are not familiar with programming rest easy, it's just a few steps.

* Installing Python
* Installing Packages
* Create a throwaway Gmail account
* Editing the script for your clinic
* Setting the script to run on a schedule


Installing Python
^^^^^^^^^^^^^^^^^

The script uses Python on the backend. Go to the Python `download page <https://www.python.org/downloads/>`_ and install
`Python 3 <https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe>`_.

.. image:: images/python_install.png

.. note::

     You must install Python 3.x, not Python 2.x.

.. note::

    During installation, when prompted select "Add to PATH". This will allow you to use Python from the command line.

Installing Packages
^^^^^^^^^^^^^^^^^^^

.. note::

    If you know what you're doing, set up a venv or use conda rather that the base env.

Now that Python is installed we need to install a few extra Python libraries. Assuming you are on Windows open a command
line terminal (you can do this by opening the start menu and typing "cmd"). In the terminal type the following:

.. code-block:: bash

    pip install pylinac yagmail

This command installs the two libraries needed to analyzed trajectory logs and to send you an email.

Create a throwaway Gmail account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To send emails, the script needs an email service provider, specifically Gmail. Create one `here <https://accounts.google.com/signupwithoutgmail?hl=en-GB>`_.

.. warning::

It is **strongly** recommended to create
a throwaway account and not use your personal or work gmail accounts.

Once your account is made, you will need to turn "Less secure apps" on. Do that `here <https://myaccount.google.com/lesssecureapps>`_
when logged in under the throwaway account.


Editing the script for your clinic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The script (viewable `here <https://github.com/jrkerns/MLCAlert/blob/master/mlc_alert.py>`_) needs a few settings
tweaked for your particular clinic.

First, `download <https://github.com/jrkerns/MLCAlert/archive/master.zip>`_ the script to a known location.
Now, use a text editor to open the `mlc_alert.py` file. You can use Notepad (it will be a bit garbled) or
something more powerful like `Notepad++ <https://notepad-plus-plus.org/>`_.

After the file is open, edit `lines 10-25 <https://github.com/jrkerns/MLCAlert/blob/master/mlc_alert.py#L10-L25>`_
to match your clinic. The settings are described below:

* `LOG_FOLDER` will be where your trajectory logs are stored on the I: drive.

.. note::

      If you are on Windows be sure the string has an "r" in front of it (e.g. r'I:/SN 1234/...').

* `MACHINE_NAME` is the name of your machine; it is only used in the subject of the email so you know which machine it is referring to.

For `LEAF_DEVIATION_THRESHOLD_MM`, `LEAF_DEVIATION_NUMBER_PER_DAY`, `ANALYSIS_WINDOW_DAYS`, and `DAYS_WITH_DEVIATIONS_WITHIN_WINDOW`,
it is best to read the paper. Unfortunately, the authors use unintuitive terms like `a` to describe these parameters.

* `GMAIL_UN` is the name of the gmail account you just set up.
* `GMAIL_PW` is the password for the gmail account.
* `RECIPIENTS` is a list of people that should get the email when it triggers.

Setting the script to run on a schedule
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At this point you can run the script. However, the idea is to run it regularly so you can be alerted when a motor needs replacing.

To run it one-off and verify no errors occur, you can open a command line terminal (as above) and type:

.. code-block:: bash

    python C:/path/to/mlc_alert.py

where of course the path points to the alert.py file.

To set the script on a schedule simply assign it using Windows Task Scheduler. This general process can be found
`here <https://pylinac.readthedocs.io/en/latest/watcher.html#using-the-watcher-with-windows-task-scheduler>`_. The only
differences from that list of instructions is instead of creating a new separate script file you will directly point to
this mlc_alert.py file.

